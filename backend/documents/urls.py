from django.urls import path
from .views import file_watermarked, signer_pdf, telecharger_cle_publique, verifier_pdf, DiplomaListCreateView, \
    DiplomaDetailView, DemandeSoumissionDetailView, \
    DemandeSoumissionListCreateView, demande_soumission_status, type_diplome_status, SauvegardeJSON

urlpatterns = [
    path('download-document/<path:url>/', file_watermarked, name='download-document'),
    path('signe-document/<path:url>/', signer_pdf, name='signe-document'),
    path('download-public-key/', telecharger_cle_publique, name='download-public-key'),
    path('verify-document/', verifier_pdf, name='verify-document'),

    path('diplomas/', DiplomaListCreateView.as_view(), name='diploma-list-create'),
    path('diplomas/<str:pk>/', DiplomaDetailView.as_view(), name='diploma-detail'),
    path('demande-soumission/', DemandeSoumissionListCreateView.as_view(), name='demande-soumission-list-create'),
    path('demande-soumission/<str:pk>/', DemandeSoumissionDetailView.as_view(), name='demande-soumission-detail'),
    path('demande-soumission-status/', demande_soumission_status, name='demande-soumission-status'),
    path('type-diplome-status/', type_diplome_status, name='type-diplome-status'),

    path('sauvegarde-json/', SauvegardeJSON.as_view(), name='sauvegarde-json'),

]
