from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader, PdfWriter
import os
import requests

TEXT = "Sidy, this is a test."
WATERMARK = os.path.join(os.getcwd(), "watermark.pdf")


def makeWatermark():
    pdf = canvas.Canvas(WATERMARK, pagesize=A4)
    pdf.translate(inch, inch)
    pdf.setFillColor(colors.grey, alpha=0.6)
    pdf.setFont("Helvetica", 50)
    pdf.rotate(45)
    pdf.drawCentredString(400, 100, TEXT)
    pdf.save()

def download_pdf_file(url: str) -> str:
    """Télécharge un PDF depuis une URL donnée, applique un filigrane et renvoie le chemin du fichier.

    :param url: L'URL du fichier PDF à télécharger
    :return: Le chemin du fichier PDF téléchargé et filigrané, ou une chaîne vide en cas d'échec.
    """

    # Création du filigrane si nécessaire
    if not os.path.exists(WATERMARK):
        makeWatermark()

    # Requête URL et obtention de l'objet réponse
    response = requests.get(url, stream=True)

    # Isolation du nom du fichier PDF de l'URL
    pdf_file_name = os.path.basename(url)
    if response.status_code == 200:
        # Sauvegarde dans le répertoire courant
        os.makedirs("diplomas_downloaded/", exist_ok=True)
        filepath = os.path.join("diplomas_downloaded/", pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)

        # Ajout du filigrane
        watermark = PdfReader(open(WATERMARK, "rb")).pages[0]
        reader = PdfReader(filepath)
        writer = PdfWriter()

        for page in reader.pages:
            page.merge_page(watermark)
            writer.add_page(page)

        # Écrire le nouveau PDF avec le filigrane
        with open(filepath, 'wb') as output_pdf:
            writer.write(output_pdf)

        print(f'{pdf_file_name} was successfully saved and watermarked!')
        return filepath  # Retourne le chemin du fichier PDF
    else:
        print(f'Uh oh! Could not download {pdf_file_name},')
        print(f'HTTP response status code: {response.status_code}')
        return ""  # Retourne une chaîne vide en cas d'échec
