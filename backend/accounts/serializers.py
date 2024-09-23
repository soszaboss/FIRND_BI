from rest_framework import serializers
from .models import Account



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
            'password': {'write_only': True, 'required': True},
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
            role=Account.Role.DIPLOME
        )
        user.save()
        return user


class InstitutionUserSerializer(CreateUserSerializer):

    def create(self, validated_data):
        user = Account.objects.create_user(
            email=validated_data['email'],
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
            role=Account.Role.ADMIN
        )
        user.save()
        return user

