from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


from accounts.views import DiplomeUserList, InstitutionUserList
from authentication.views import EntrepriseCreateView

#from diplome.views import FilesViewSet


router = routers.DefaultRouter()

#router.register(r'files', FilesViewSet, basename='files')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api-authentication/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('authentication.urls')),
    path('users/', include('accounts.urls')),
    # path('diplome/', include('diplome.urls')),
    path('auth/diplome/register/', DiplomeUserList.as_view(), name='diplome-register'),
    # path('users/institutions/', InstitutionUserList.as_view(), name='institution-user-list'),
    path('institutions/', InstitutionUserList.as_view(), name='institution-user-list'),
    path('entreprises/', EntrepriseCreateView.as_view(), name='entreprise-create'),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
