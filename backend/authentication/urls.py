from django.urls import path
from .views import LoginViewViaMail, VerifyOTPView, LoginViewViaSms, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Replace the default TokenObtainPairView with your custom view
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URL pour la gestion du processus d'OTP
    path('login/', LoginViewViaMail.as_view(), name='login'),
    path('verify-otp-via-email/', VerifyOTPView.as_view(), name='verify-otp-via-mail'),
    #path('verify-otp-via-sms/', LoginViewViaSms.as_view(), name='verify-otp-via-sms'),
]
