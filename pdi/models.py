from pyexpat import model
from django.db import models

# Create your models here.
class Department(models.Model):
   name = models.CharField(max_length=50, unique=True)
   description = models.CharField(max_length=255, blank=True, null=True)

   def __str__(self):
      return self.name

class Employee(models.Model):
   first_name = models.CharField(max_length=50)
   last_name = models.CharField(max_length=50)
   email = models.EmailField()
   department = models.ForeignKey(Department, models.PROTECT, blank=True, null=True)

   @property
   def name(self):
      return f'{self.first_name} {self.last_name}'

   def __str__(self):
      return self.name