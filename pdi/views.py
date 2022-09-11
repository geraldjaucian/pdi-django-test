import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

# Create your views here.
def export_view(req):
   buffer = io.BytesIO()
   p = canvas.Canvas(buffer)

   # Draw things on the PDF. Here's where the PDF generation happens.
   # See the ReportLab documentation for the full list of functionality.
   p.drawString(100, 100, "Hello world.")

   # Close the PDF object cleanly, and we're done.
   p.showPage()
   p.save()

   # FileResponse sets the Content-Disposition header so that browsers
   # present the option to save the file.
   buffer.seek(0)
   return FileResponse(buffer, as_attachment=True, filename='hello.pdf')