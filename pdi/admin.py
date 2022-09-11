import csv
from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField
from django.contrib.auth import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
import pdfkit

from .models import Employee, Department

# Register your models here.
admin.site.site_title = "Philippine Daily Inquirer"
admin.site.site_header = "Philippine Daily Inquirer"

admin.site.unregister([models.Group, models.User])


class GroupAdminForm(ModelForm):
   class Meta:
      model = models.Group
      fields = ('name', 'permissions')
   permissions = ModelMultipleChoiceField(
      models.Permission.objects
         .exclude(content_type__app_label__in=['admin', 'contenttypes', 'sessions'])
         .exclude(content_type__model__in=['permission']),
      widget=admin.widgets.FilteredSelectMultiple(('permissions'), False))

@admin.register(models.Group)
class GroupModelAdmin(ModelAdmin):
   form = GroupAdminForm
   search_fields = ['name']
   # fields = ('permissions',)
   list_display = ('name', 'permissions_codename')
   ordering = ['name']

   def permissions_codename(self, obj):
      return ", ".join([p.codename for p in obj.permissions.all()]) 


@admin.register(models.User)
class UserModelAdmin(UserAdmin):
   list_display = ('username', 'email', 'is_active', 'is_superuser')
   search_fields = ('username', 'email')
   fieldsets = (
      (None, {'fields': ('username', 'email', 'password')}),
      (('MSC'), {
         'fields': ('is_active', 'is_superuser', 'groups'),
      }),
      (('Important dates'), {'fields': ('last_login', 'date_joined')}),
   )
   list_filter = ('is_superuser', 'is_active', 'groups')
   add_fieldsets = (
      (None, {
         'classes': ('wide',),
         'fields': ('username', 'email', 'password1', 'password2'),
      }),
      ('MSC', {
         'classes': ('wide',),
         'fields': ('groups', 'is_active', 'is_superuser'),
      }),
   )

   def save_model(self, req, obj, form, change):
      obj.is_staff = True
      obj.save()


@admin.register(Department)
class DepartmentModelAdmin(ModelAdmin):
   list_display = ('name', 'description')
   search_fields = ('name', 'description')

@admin.register(Employee)
class EmployeeModelAdmin(ModelAdmin):
   list_display = ('name', 'email', 'department')
   search_fields = ('first_name', 'last_name', 'email')
   list_filter = ('department',)


# ACTIONS

@admin.action(permissions=['view'], description='Export selected as .csv')
def export_as_csv(m, req, qs):
   meta = m.model._meta
   field_names = [field.name for field in meta.fields]

   response = HttpResponse(content_type='text/csv')
   response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
   writer = csv.writer(response)
   writer.writerow(field_names)
   for obj in qs:
      writer.writerow([getattr(obj, field) for field in field_names])

   return response
admin.site.add_action(export_as_csv)

@admin.action(permissions=['view'], description='Export selected as .json')
def export_as_json(m, req, qs):
   response = HttpResponse(content_type="application/json")
   response['Content-Disposition'] = 'attachment; filename={}.json'.format(qs.model.__module__)
   serializers.serialize("json", qs, stream=response)
   return response
admin.site.add_action(export_as_json)

@admin.action(permissions=['view'], description='Export selected as .xml')
def export_as_xml(m, req, qs):
   response = HttpResponse(content_type="application/xml")
   response['Content-Disposition'] = 'attachment; filename={}.xml'.format(qs.model.__module__)
   serializers.serialize("xml", qs, stream=response)
   return response
admin.site.add_action(export_as_xml)