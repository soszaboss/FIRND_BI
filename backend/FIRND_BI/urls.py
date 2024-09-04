from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from diplome.views import FilesViewSet, file_watermarked
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()

router.register(r'files', FilesViewSet, basename='files')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('diplome/', include('diplome.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
