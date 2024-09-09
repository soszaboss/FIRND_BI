from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    # url d'authentification pour recuperer le refresh et l'access token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # url pour le refresh des token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
