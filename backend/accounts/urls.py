from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import AdminUserList, DiplomeUserList, InstitutionUserList, UsersList

urlpatterns = [

    # url pour voir les utilisateurs avec le role d'admin avec une method get,
    # et créer un utilisateur avec le role d'admin avec une methode post.
    path('admins/', AdminUserList.as_view(), name='admin-user-list'),

    # url pour voir les utilisateurs avec le role de diplomé une method get,
    # et créer un utilisateur avec le role de diplomé une methode post.
    path('diplomes/', DiplomeUserList.as_view(), name='diplomé-user-list'),

    # url pour voir les utilisateurs administrateurs avec une method get,
    # et créer un utilisateur avec le role d'institution une methode post.
    path('institutions/', InstitutionUserList.as_view(), name='institution-user-list'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),


    # url pour voir tous les utilisateurs
    path('', UsersList.as_view(), name='user-list'),
]
