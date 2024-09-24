from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from documents.views import FilesViewSet, EtudiantsViewSet
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

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
