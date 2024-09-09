from rest_framework import serializers
from .models import Account


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        exclude = ['is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
            'role':{'write_only': True},
        }


class DiplomeUserSerializer(CreateUserSerializer):

    def create(self, validated_data):
        user = Account().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=Account.Role.DIPLOME
        )
        user.save()
        return user


class InstitutionUserSerializer(CreateUserSerializer):

    def create(self, validated_data):
        user = Account().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=Account.Role.INSTITUTION
        )
        user.save()
        return user


class AdminUserSerializer(CreateUserSerializer):

    def create(self, validated_data):
        user = Account().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=Account.Role.ADMIN
        )
        user.save()
        return user

