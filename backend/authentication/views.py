from rest_framework.views import APIView
from rest_framework import status
from accounts.models import Account
from .utils.functions import get_tokens_for_user
from .utils.send_otp import send_otp_via_mail
from datetime import timedelta
from random import randint
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate


class LoginView(APIView):
    """Vue pour gérer l'authentification avec OTP."""

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response("L'email et le mot de passe sont requis.", status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response("Identifiants invalides.", status=status.HTTP_400_BAD_REQUEST)

        # Vérification du nombre maximum de tentatives d'OTP
        if user.max_otp_try <= 0 and user.otp_max_out and timezone.now() < user.otp_max_out:
            return Response("Nombre maximum de tentatives OTP atteint, réessayez dans une heure", status=status.HTTP_400_BAD_REQUEST)

        # Génération de l'OTP et mise à jour des champs de l'utilisateur
        otp = randint(1000, 9999)
        otp_expiry = timezone.now() + timedelta(minutes=10)
        user.otp = otp
        user.otp_expiry = otp_expiry
        user.max_otp_try -= 1

        # Réinitialisation des tentatives d'OTP
        if user.max_otp_try == 0:
            user.otp_max_out = timezone.now() + timedelta(hours=1)
        elif user.max_otp_try < 0:
            user.max_otp_try = 3
            user.otp_max_out = None

        user.save()
        send_otp_via_mail(otp, user.email)
        return Response({"message":"OTP généré avec succès, veuillez vérifier votre adresse mail", "user_id":user.id}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    """Vue pour vérifier le code OTP."""

    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        user_id = request.data.get('user_id')

        if not otp:
            return Response("Veuillez entrer un OTP.", status=status.HTTP_400_BAD_REQUEST)
        if not user_id:
            return Response("Veuillez entrer un user_id.", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Account.objects.get(otp=otp, id=user_id)
        except Account.DoesNotExist:
            return Response("Identifiants invalides.", status=status.HTTP_400_BAD_REQUEST)

        # Vérification de l'expiration de l'OTP
        if user.otp_expiry and timezone.now() > user.otp_expiry:
            return Response("Le code OTP a expiré. Veuillez en demander un nouveau.", status=status.HTTP_400_BAD_REQUEST)

        # Connexion de l'utilisateur après vérification OTP
        login(request, user)

        # Réinitialisation des champs liés à l'OTP
        user.otp = None
        user.otp_expiry = None
        user.max_otp_try = 3
        user.otp_max_out = None
        user.save()

        # Génération des tokens JWT
        refresh = RefreshToken.for_user(user)
        return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)

