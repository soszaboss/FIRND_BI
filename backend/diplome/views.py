from rest_framework import status, viewsets
from  rest_framework.decorators import api_view
from .models import Diploma
from .serializers import FileSerializer
from .utils.download_and_watermark_document import download_pdf_file
from rest_framework.response import Response
from django.http import FileResponse
import os


class FilesViewSet(viewsets.ModelViewSet):
    queryset = Diploma.objects.all()
    serializer_class = FileSerializer


@api_view(['GET'])
def file_watermarked(request, url):
    # Télécharger le fichier PDF et appliquer le filigrane
    filepath = download_pdf_file(url)

    if filepath:
        # Ouvrir le fichier sans gestionnaire de contexte pour qu'il reste ouvert
        pdf_file = open(filepath, 'rb')
        try:
            response = FileResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(filepath)}'

            # Planifier la suppression du fichier après l'envoi
            def delete_file_after_response(response):
                pdf_file.close()  # Fermer le fichier après que la réponse ait été envoyée
                if os.path.exists(filepath):
                    os.remove(filepath)

            response.close = delete_file_after_response
            return response
        except Exception as e:
            pdf_file.close()  # Fermer le fichier en cas d'exception
            if os.path.exists(filepath):
                os.remove(filepath)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "Failed to download and watermark the PDF."}, status=status.HTTP_400_BAD_REQUEST)