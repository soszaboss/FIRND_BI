from django.http import JsonResponse, FileResponse
from rest_framework.decorators import api_view
from rest_framework import status
import hashlib
import requests
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import os

# Fonction pour télécharger le PDF à partir d'un lien HTTPS
def telecharger_pdf(lien_pdf, chemin_de_destination):
    try:
        reponse = requests.get(lien_pdf)
        if reponse.status_code == 200:
            with open(chemin_de_destination, 'wb') as fichier_pdf:
                fichier_pdf.write(reponse.content)
            return True
        else:
            return False
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        return False

# Fonction pour hasher le contenu du PDF
def hasher_pdf(chemin_pdf):
    with open(chemin_pdf, 'rb') as fichier_pdf:
        contenu = fichier_pdf.read()
        hash_obj = hashlib.sha256(contenu)
        return hash_obj.hexdigest(), contenu

# Fonction pour signer le hash avec une clé privée
def signer_hash(hash_contenu, cle_privee):
    cle_privee_obj = RSA.import_key(cle_privee)
    hash_obj = SHA256.new(hash_contenu.encode('utf-8'))
    signature = pkcs1_15.new(cle_privee_obj).sign(hash_obj)
    return signature

# Fonction pour générer une paire de clés RSA (clé publique et clé privée)
def generer_paire_de_cles():
    cle_privee = RSA.generate(2048)
    cle_publique = cle_privee.publickey().export_key()
    return cle_privee.export_key(), cle_publique

@api_view(['POST'])
def signer_pdf(request):
    try:
        # Récupération du lien PDF depuis la requête POST
        lien_pdf = request.data.get('lien_pdf')
        if not lien_pdf:
            return JsonResponse({"erreur": "Le lien PDF est requis"}, status=status.HTTP_400_BAD_REQUEST)

        # Téléchargement du fichier PDF
        chemin_pdf = "document.pdf"
        telecharge_succes = telecharger_pdf(lien_pdf, chemin_pdf)
        if not telecharge_succes:
            return JsonResponse({"erreur": "Impossible de télécharger le fichier PDF"}, status=status.HTTP_400_BAD_REQUEST)

        # Hasher le fichier PDF
        hash_pdf, contenu_pdf = hasher_pdf(chemin_pdf)

        # Générer des clés RSA (clé privée et publique)
        cle_privee, cle_publique = generer_paire_de_cles()

        # Signer le hash du PDF
        signature = signer_hash(hash_pdf, cle_privee)

        # Enregistrer le fichier signé et la clé publique
        chemin_pdf_signe = "document_signe.pdf"
        chemin_signature = "signature.bin"
        chemin_cle_publique = "cle_publique.pem"

        # Sauvegarder la signature
        with open(chemin_signature, 'wb') as fichier_signature:
            fichier_signature.write(signature)

        # Sauvegarder le PDF (non modifié dans cet exemple, mais vous pouvez ajouter des métadonnées)
        with open(chemin_pdf_signe, 'wb') as fichier_pdf:
            fichier_pdf.write(contenu_pdf)

        # Sauvegarder la clé publique
        with open(chemin_cle_publique, 'wb') as fichier_cle_publique:
            fichier_cle_publique.write(cle_publique)

        # Retourner le fichier PDF signé et la clé publique
        return JsonResponse({
            "message": "Le document a été signé avec succès.",
            "lien_pdf_signe": f"/telecharger-pdf/{chemin_pdf_signe}",
            "lien_cle_publique": f"/telecharger-cle/{chemin_cle_publique}"
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"erreur": f"Une erreur s'est produite : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def telecharger_pdf_signe(request, filename):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    return JsonResponse({"erreur": "Fichier non trouvé"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def telecharger_cle_publique(request, filename):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    return JsonResponse({"erreur": "Fichier non trouvé"}, status=status.HTTP_404_NOT_FOUND)
