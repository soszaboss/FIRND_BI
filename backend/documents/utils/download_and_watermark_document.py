from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader, PdfWriter
import os
import requests
from rest_framework import status
from rest_framework.response import Response

TEXT = "Sidy, this is a test."
WATERMARK = os.path.join(os.getcwd(), "watermark.pdf")

def download_and_save_document(url: str):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        pdf_file_name = os.path.basename(url)
        os.makedirs("downloaded_documents/", exist_ok=True)
        filepath = os.path.join("downloaded_documents/", pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
        return filepath
    return None  # Ajout d'une gestion d'erreur en cas d'échec

def makeWatermark():
    pdf = canvas.Canvas(WATERMARK, pagesize=A4)
    pdf.translate(inch, inch)
    pdf.setFillColor(colors.grey, alpha=0.6)
    pdf.setFont("Helvetica", 50)
    pdf.rotate(45)
    pdf.drawCentredString(400, 100, TEXT)
    pdf.save()

def download_pdf_file(url: str) -> str | Response:
    if not os.path.exists(WATERMARK):
        makeWatermark()

    filepath = download_and_save_document(url)
    if filepath:  # Vérifier si le téléchargement a réussi
        watermark = PdfReader(open(WATERMARK, "rb")).pages[0]
        reader = PdfReader(filepath)
        writer = PdfWriter()

        for page in reader.pages:
            page.merge_page(watermark)
            writer.add_page(page)

        # Écrire le nouveau PDF avec le filigrane
        with open(filepath, 'wb') as output_pdf:
            writer.write(output_pdf)
        return filepath
    else:
        return Response({"message": "Échec du téléchargement du fichier PDF."}, status=status.HTTP_400_BAD_REQUEST)
