from django.urls import path
from .views import LoginView, VerifyOTPView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # URL d'authentification pour récupérer les tokens JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URL pour la gestion du processus d'OTP
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    # Route pour obtenir le token JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Route pour rafraîchir le token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
