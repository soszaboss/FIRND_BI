from django.urls import path
from .views import file_watermarked, signer_pdf, telecharger_cle_publique, verifier_pdf

urlpatterns = [
    path('download-document/<path:url>/', file_watermarked, name='download-document'),
    path('signe-document/<path:url>/', signer_pdf, name='signe-document'),
    path('download-public-key/', telecharger_cle_publique, name='download-public-key'),
    path('verify-document/', verifier_pdf, name='verify-document'),
]
