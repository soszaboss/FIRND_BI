from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import serializers
from .models import Account
import string
import random

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def send_email_to_activate_account(user, password):
    mail_subject = 'Activate your account.'
    message = f"Password: {password}"
    to_email = user.email
    send_email = EmailMessage(
        subject=mail_subject,
        from_email=settings.EMAIL_HOST_USER,
        body=message,
        to=[to_email]
    )
    send_email.send()

class CreateUserSerializer(serializers.ModelSerializer):
    """
        Création d'un serializer pour la de création de comptes utilisateurs
        avec une gestion de differentes roles ( admin, institution, diplomé )
    """
    class Meta:
        model = Account

        # exclusion des champs ci-dessous lors de l'affichage et saisie des données
        fields = ['username' ,'phone_number','password', 'email', 'role', 'last_login', 'is_active']

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'role':{'read_only': True},
            'last_login':{'read_only': True},
            'is_active':{'read_only': True},
        }


# chacun des 3 classes ci-dessous se charge de la création de compte utilisateur pour chaque different role

class DiplomeUserSerializer(CreateUserSerializer):

    def create(self, validated_data):
        user = Account.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number = validated_data['phone_number'],
            role=Account.Role.DIPLOME
        )
        user.save()
        return user


class InstitutionUserSerializer(CreateUserSerializer):

    def create(self, validated_data):
        user = Account.objects.create_user(
            email=validated_data['email'],
            phone_number = validated_data['phone_number'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=Account.Role.INSTITUTION
        )
        user.save()
        return user


class AdminUserSerializer(CreateUserSerializer):

    def create(self, validated_data):
        user = Account.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number = validated_data['phone_number'],
            username=validated_data['username'],
            role=Account.Role.ADMIN
        )
        user.save()
        return user


class EmployeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account

        # exclusion des champs ci-dessous lors de l'affichage et saisie des données
        fields = ['username', 'phone_number', 'email', 'role', 'last_login', 'is_active']

        extra_kwargs = {
            'email': {'required': True},
            'role': {'read_only': True},
            'last_login': {'read_only': True},
            'is_active': {'read_only': True},
        }
    def create(self, validated_data):
        password = generate_random_password()
        user = Account.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            password=password,
            role=Account.Role.EMPLOYE
        )
        user.save()
        send_email_to_activate_account(user, password)
        return user
