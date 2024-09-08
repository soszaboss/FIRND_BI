import spacy
import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Charger le modèle de langue de spaCy
nlp = spacy.load("en_core_web_sm")

# Fonction pour détecter les champs sensibles à masquer via IA
def detect_sensitive_fields(text):
    doc = nlp(text)
    sensitive_fields = []
    for ent in doc.ents:
        if ent.label_ in ["Nom", "Mention"]:  # Détection
            sensitive_fields.append(ent.text)
    return sensitive_fields
