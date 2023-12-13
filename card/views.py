# views.py
import textwrap

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image, ImageDraw, ImageOps
from reportlab.platypus import Paragraph

from card.models import Student

class IDCardPDFView(View):

    def get(self, request, pk):
        # Fetch user information from the model (replace with your actual model)
        user = get_object_or_404(Student, pk=pk)

        # Create a BytesIO buffer to save the PDF
        buffer = BytesIO()

        # Create a ReportLab PDF document
        pdf = canvas.Canvas(buffer)

        # Load the ID card template image
        template_image_path = "static/images/id_card_template.jpeg"
        template_image = Image.open(template_image_path)

        # Set the size of the PDF to match the template image
        pdf.setPageSize(template_image.size)

        # Draw the template image onto the PDF
        pdf.drawInlineImage(template_image_path, 0, 0, width=template_image.size[0], height=template_image.size[1])

        # Add user information to the PDF
        pdf.setFont("Helvetica-Bold", 40)

        name_x_position = template_image.size[0] / 2

        pdf.drawCentredString(name_x_position, 500, user.name)
        pdf.setFont("Helvetica-Bold", 30)

        pdf.drawCentredString(name_x_position, 450, user.session)

        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(260, 400, user.admission)
        pdf.drawString(260, 370, user.father_name)
        pdf.drawString(260, 340, user.mother_name)
        pdf.drawString(260, 310, str(user.dob))
        pdf.drawString(260, 280, user.standard)
        pdf.drawString(260, 255, user.contact_no)

        styles = getSampleStyleSheet()

        address_style = ParagraphStyle(
            'AddressStyle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',  # Specify the desired font
            fontSize=20,  # Specify the desired font size
            leading=18,
            spaceAfter=20,
            spaceBefore=12,
        )
        small_rows = textwrap.wrap(user.address, width=30)
        y = 225
        for row in small_rows:
            pdf.drawString(260, y, row)
            y -= 20
        # Load the user image
        user_image_path = user.photo
        user_image = Image.open(user_image_path)

        # Paste the circular user image onto the PDF
        pdf.drawInlineImage(user_image, name_x_position - 142, 558, width=288, height=288)

        # Save the PDF to the buffer
        pdf.save()

        # Rewind the buffer to the beginning
        buffer.seek(0)

        # Create a Django response with the PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename={user.name}_id_card.pdf'
        response.write(buffer.read())

        return response
