from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse
import os

from .models import Diploma
from .serializers import FileSerializer
from .utils.download_and_watermark_document import download_pdf_file, download_and_save_document
from .utils.signature import hasher_pdf, generer_paire_de_cles, signer_hash
from .utils.verification import verifier_signature


def return_pfd_file(filepath: str):
    try:
        pdf_file = open(filepath, 'rb')
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(filepath)}'

        def delete_file_after_response(response):
            pdf_file.close()
            if os.path.exists(filepath):
                os.remove(filepath)

        # Assigning the correct closure method with response argument
        response.close = lambda: delete_file_after_response(response)
        return response
    except Exception as e:
        # Ensure pdf_file is properly defined before calling close
        if 'pdf_file' in locals():
            pdf_file.close()
        if os.path.exists(filepath):
            os.remove(filepath)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilesViewSet(viewsets.ModelViewSet):
    queryset = Diploma.objects.all()
    serializer_class = FileSerializer

@api_view(['GET'])
def file_watermarked(request, url):
    filepath = download_pdf_file(url)
    if filepath:
        return return_pfd_file(filepath)
    else:
        return Response({"error": "Échec du téléchargement et du filigrane du PDF."}, status=status.HTTP_400_BAD_REQUEST)


chemin_signature = "./documents/utils/signature et cle publique/signature.bin"
chemin_cle_publique = "./documents/utils/signature et cle publique/cle_publique.pem"

from django.http import FileResponse, HttpResponse
from rest_framework.decorators import api_view
import os

@api_view(['POST'])
def signer_pdf(request, url):
    try:
        # Télécharger et sauvegarder le document
        document = download_and_save_document(url)

        # Hacher le PDF et obtenir son contenu
        hash_pdf, contenu_pdf = hasher_pdf(document)

        # Générer une paire de clés (privée et publique)
        cle_privee, cle_publique = generer_paire_de_cles()

        # Signer le hash du PDF avec la clé privée
        signature = signer_hash(hash_pdf, cle_privee)

        # Sauvegarder la signature dans un fichier
        with open(chemin_signature, 'wb') as fichier_signature:
            fichier_signature.write(signature)
            fichier_signature.close()

        # Réécrire le contenu du PDF dans le fichier
        with open(document, 'wb') as fichier_pdf:
            fichier_pdf.write(contenu_pdf)
            fichier_pdf.close()

        # Sauvegarder la clé publique dans un fichier
        with open(chemin_cle_publique, 'wb') as fichier_cle_publique:
            fichier_cle_publique.write(cle_publique)
            fichier_cle_publique.close()

        pdf_file = open(document, 'rb')
        # Créer une réponse de fichier pour renvoyer le PDF signé
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(document)}"'

        return response

    except Exception as e:
        # Gestion des exceptions et retour d'un message d'erreur approprié
        return HttpResponse(f"Erreur lors de la signature du PDF: {str(e)}", status=500)


@api_view(['GET'])
def telecharger_cle_publique(request):
    file_path = chemin_cle_publique
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    return Response({"erreur": "Fichier non trouvé"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def verifier_pdf(request):
    try:
        # Récupérer le fichier PDF depuis la requête
        fichier_pdf = request.FILES.get('pdf')

        if not fichier_pdf:
            return Response({"message": "Veuillez insérer un document."}, status=status.HTTP_400_BAD_REQUEST)

        # Sauvegarder le fichier PDF téléchargé
        pdf_file_name = 'verification_document.pdf'
        os.makedirs("downloaded_documents/", exist_ok=True)
        filepath = os.path.join("downloaded_documents/", pdf_file_name)
        with open(filepath, 'wb') as pdf_file:
            for chunk in fichier_pdf.chunks():
                pdf_file.write(chunk)


        signature = open(chemin_signature, 'rb').read()
        cle_publique = open(chemin_cle_publique, 'rb').read()

        # Hacher le contenu du PDF
        hash_pdf = hasher_pdf(filepath)

        # Vérifier la signature avec le hash et la clé publique
        est_valide = verifier_signature(hash_pdf, signature, cle_publique)

        # Retourner le résultat
        if est_valide:
            return Response({"message": "La signature est valide."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "La signature n'est pas valide."}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"erreur": f"Une erreur s'est produite : {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
