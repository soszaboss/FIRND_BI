from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from documents.views import (
    FilesViewSet, EtudiantsViewSet, CreatePDFView, DemandeSoumissionStatusView,
    FileWatermarkedView, TelechargerClePubliqueView, GetPDFView, GetSubmissionView,
    SignerPDFView, TelechargeView, TypeDiplomeStatusView, VerifierPDFView
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView



router = routers.DefaultRouter()

router.register(r'files', FilesViewSet, basename='files')
router.register(r'etudiants', EtudiantsViewSet, basename='etudiants')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api-authentication/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('authentication.urls')),
    path('users/', include('accounts.urls')),
    path('documents/', include('documents.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('create-pdf/', CreatePDFView.as_view(), name='create-pdf'),
    path('demande-soumission-status/', DemandeSoumissionStatusView.as_view(), name='demande-soumission-status'),
    path('file-watermarked/<path:url>/', FileWatermarkedView.as_view(), name='file-watermarked'),
    path('telecharger-cle-publique/', TelechargerClePubliqueView.as_view(), name='telecharger-cle-publique'),
    path('get-pdf/', GetPDFView.as_view(), name='get-pdf'),
    path('get-submission/', GetSubmissionView.as_view(), name='get-submission'),
    path('signer-pdf/<path:url>/', SignerPDFView.as_view(), name='signer-pdf'),
    path('telecharge/<int:id>/', TelechargeView.as_view(), name='telecharge'),
    path('type-diplome-status/', TypeDiplomeStatusView.as_view(), name='type-diplome-status'),
    path('verifier-pdf/', VerifierPDFView.as_view(), name='verifier-pdf'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
