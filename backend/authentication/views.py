from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import Account
from .utils.functions import get_tokens_for_user
from .utils.send_otp import send_otp_via_mail, send_opt_via_sms
from datetime import timedelta
from random import randint
from django.contrib.auth import login
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import VerifyOTPSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .backends import CustomAuthBackend  # Import your custom backend

class LoginViewViaMail(GenericAPIView):
    """Vue pour gérer l'authentification avec OTP via email."""
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_description="Login with email and password to receive an OTP via email",
        responses={
            200: openapi.Response(
                description="OTP généré avec succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        if not email or not password:
            return Response({"error": "L'email et le mot de passe sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"error": "Identifiants invalides."}, status=status.HTTP_400_BAD_REQUEST)

        if user.max_otp_try <= 0 and user.otp_max_out and timezone.now() < user.otp_max_out:
            return Response({"error": "Nombre maximum de tentatives OTP atteint, réessayez dans une heure"}, status=status.HTTP_400_BAD_REQUEST)

        otp = randint(1000, 9999)
        otp_expiry = timezone.now() + timedelta(minutes=10)
        user.otp = otp
        user.otp_expiry = otp_expiry
        user.max_otp_try -= 1

        if user.max_otp_try == 0:
            user.otp_max_out = timezone.now() + timedelta(hours=1)
        elif user.max_otp_try < 0:
            user.max_otp_try = 3
            user.otp_max_out = None

        user.save()
        send_otp_via_mail(otp, user.email)
        return Response({"message": "OTP généré avec succès, veuillez vérifier votre adresse email"}, status=status.HTTP_200_OK)

class LoginViewViaSms(GenericAPIView):
    """Vue pour gérer l'authentification avec OTP via SMS."""
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_description="Login with email and password to receive an OTP via SMS",
        responses={
            200: openapi.Response(
                description="OTP généré avec succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        if not email or not password:
            return Response({"error": "L'email et le mot de passe sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"error": "Identifiants invalides."}, status=status.HTTP_400_BAD_REQUEST)

        if user.max_otp_try <= 0 and user.otp_max_out and timezone.now() < user.otp_max_out:
            return Response({"error": "Nombre maximum de tentatives OTP atteint, réessayez dans une heure"}, status=status.HTTP_400_BAD_REQUEST)

        otp = randint(1000, 9999)
        otp_expiry = timezone.now() + timedelta(minutes=10)
        user.otp = otp
        user.otp_expiry = otp_expiry
        user.max_otp_try -= 1

        if user.max_otp_try == 0:
            user.otp_max_out = timezone.now() + timedelta(hours=1)
        elif user.max_otp_try < 0:
            user.max_otp_try = 3
            user.otp_max_out = None

        user.save()
        send_opt_via_sms(otp, user.phone_number)
        return Response({"message": "OTP généré avec succès, veuillez vérifier votre téléphone"}, status=status.HTTP_200_OK)

class VerifyOTPView(GenericAPIView):
    """Vue pour vérifier le code OTP."""
    serializer_class = VerifyOTPSerializer

    @swagger_auto_schema(
        operation_description="Verify the OTP code",
        responses={
            200: openapi.Response(
                description="OTP vérifié avec succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        email = serializer.validated_data['email']

        User = get_user_model()
        try:
            user = User.objects.get(email=email, otp=otp)
        except User.DoesNotExist:
            return Response({"error": "Identifiants invalides."}, status=status.HTTP_400_BAD_REQUEST)

        # Specify the backend when logging in
        login(request, user)

        user.otp = None
        user.otp_expiry = None
        user.max_otp_try = 3
        user.otp_max_out = None
        user.save()

        return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer