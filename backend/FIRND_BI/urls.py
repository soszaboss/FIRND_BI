from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
#from diplome.views import FilesViewSet
from verification.views import verifier_pdf
from signature.views import signer_pdf, telecharger_cle_publique,telecharger_pdf_signe


router = routers.DefaultRouter()

#router.register(r'files', FilesViewSet, basename='files')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api-authentication/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('authentication.urls')),
    path('users/', include('accounts.urls')),
    path('verifier-pdf/', verifier_pdf, name='verifier_pdf'),
    path('signer-pdf/', signer_pdf, name='signer_pdf'),
    path('telecharger-pdf/<str:filename>/', telecharger_pdf_signe, name='telecharger_pdf_signe'),
    path('telecharger-cle/<str:filename>/', telecharger_cle_publique, name='telecharger_cle_publique'),

#    path('diplome/', include('diplome.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
