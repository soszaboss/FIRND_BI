from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DiplomaSerializer, DemandeSoumissionSerializer, DemandeSoumissionStatusSerializer, \
    EtudiantSerializer
from rest_framework import generics
from .models import Diploma, DemandeSoumission, DemandeSoumissionStatus, Etudiant, TypeDiplome
from django.http import FileResponse, HttpResponse
import os
from .serializers import FileSerializer
from .utils.download_and_watermark_document import download_pdf_file, download_and_save_document
from .utils.signature import hasher_pdf, generer_paire_de_cles, signer_hash
from .utils.verification import verifier_signature
from rest_framework.views import APIView
import json

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

class EtudiantsViewSet(viewsets.ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer

@api_view(['GET'])
def file_watermarked(request, url):
    filepath = download_pdf_file(url)
    if filepath:
        return return_pfd_file(filepath)
    else:
        return Response({"error": "Échec du téléchargement et du filigrane du PDF."}, status=status.HTTP_400_BAD_REQUEST)


chemin_signature = "./documents/utils/signature et cle publique/signature.bin"
chemin_cle_publique = "./documents/utils/signature et cle publique/cle_publique.pem"

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

class DiplomaListCreateView(generics.ListCreateAPIView):
    queryset = Diploma.objects.all()
    serializer_class = DiplomaSerializer


class DiplomaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diploma.objects.all()
    serializer_class = DiplomaSerializer

class DemandeSoumissionListCreateView(generics.ListCreateAPIView):
    queryset = DemandeSoumission.objects.all()
    serializer_class = DemandeSoumissionSerializer

class DemandeSoumissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DemandeSoumission.objects.all()
    serializer_class = DemandeSoumissionSerializer

@api_view(['GET'])
def demande_soumission_status(request):
    status_choices = DemandeSoumissionStatus.choices
    print(status_choices)
    data = [{'key': key, 'label': label} for key, label in status_choices]

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def type_diplome_status(request):
    status_choices = TypeDiplome.choices
    print(status_choices)
    data = [{'key': key, 'label': label} for key, label in status_choices]

    return Response(data, status=status.HTTP_200_OK)

class SauvegardeJSON(APIView):
    def post(self, request):
        data = request.data
        try:
            # Vérifier si le fichier existe déjà
            if os.path.exists(os.getcwd()+"/media/soumission.json"):
                with open(os.getcwd()+"/media/soumission.json", "r") as json_file:
                    # Charger les données existantes
                    existing_data = json.load(json_file)
            else:
                existing_data = []  # Créer une nouvelle liste si le fichier n'existe pas

            # Ajouter les nouvelles données à la liste existante
            existing_data.append(data)

            # Sauvegarder les données mises à jour dans le fichier JSON
            with open(os.getcwd()+"/media/soumission.json", "w") as json_file:
                json.dump(existing_data, json_file, indent=2)

            return Response("Données sauvegardées avec succès !", status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f"Erreur lors de la sauvegarde des données : {str(e)}",
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            # Lire les données à partir du fichier JSON
            if os.path.exists(os.getcwd()+"/media/soumission.json"):
                with open(os.getcwd()+"/media/soumission.json", "r") as json_file:
                    data = json.load(json_file)
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("Fichier non trouvé.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f"Erreur lors de la lecture des données : {str(e)}",
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)