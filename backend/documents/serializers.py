from rest_framework import serializers
from .models import Diploma

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diploma
        fields = ['user', "diploma"]