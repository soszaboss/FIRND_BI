from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import hashlib
import os

# Fonction pour hasher le contenu du PDF
def hasher_pdf(chemin_pdf):
    with open(chemin_pdf, 'rb') as fichier_pdf:
        contenu = fichier_pdf.read()
        hash_obj = hashlib.sha256(contenu)
        return hash_obj.hexdigest()

# Fonction pour vérifier la signature du hash
def verifier_signature(hash_contenu, signature, cle_publique):
    try:
        cle_publique_obj = RSA.import_key(cle_publique)
        hash_obj = SHA256.new(hash_contenu.encode('utf-8'))
        pkcs1_15.new(cle_publique_obj).verify(hash_obj, signature)
        return True
    except (ValueError, TypeError):
        return False

@api_view(['POST'])
def verifier_pdf(request):
    try:
        # Récupération des fichiers PDF, signature et clé publique depuis la requête POST
        fichier_pdf = request.FILES.get('pdf')
        fichier_signature = request.FILES.get('signature')
        fichier_cle_publique = request.FILES.get('cle_publique')

        if not fichier_pdf or not fichier_signature or not fichier_cle_publique:
            return JsonResponse({"message": "Tous les fichiers (PDF, signature, clé publique) sont requis."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Sauvegarder temporairement le fichier PDF
        chemin_pdf = 'document_verification.pdf'
        with open(chemin_pdf, 'wb') as pdf_file:
            for chunk in fichier_pdf.chunks():
                pdf_file.write(chunk)

        # Lire la signature et la clé publique
        signature = fichier_signature.read()
        cle_publique = fichier_cle_publique.read()

        # Hasher le fichier PDF pour recalculer son hash
        hash_pdf = hasher_pdf(chemin_pdf)

        # Vérifier si la signature est valide
        est_valide = verifier_signature(hash_pdf, signature, cle_publique)

        # Nettoyer les fichiers temporaires
        os.remove(chemin_pdf)

        if est_valide:
            return JsonResponse({"message": "Le document n'a pas été altéré, la signature est valide."},
                                status=status.HTTP_200_OK)
        else:
            return JsonResponse({"message": "Le document a été altéré ou la signature est invalide."},
                                status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return JsonResponse({"erreur": f"Une erreur s'est produite : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
