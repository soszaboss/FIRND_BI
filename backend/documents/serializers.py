from rest_framework import serializers
from .models import Diploma, DemandeSoumission, Etudiant


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diploma
        fields = ['etudiant', 'diploma']
class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = '__all__'

class DiplomaSerializer(serializers.ModelSerializer):
    etudiant = EtudiantSerializer(read_only=True)  # Afficher les informations des étudiants en lecture seule

    class Meta:
        model = Diploma
        fields = ['etudiant', 'full_name', 'type_diplome', 'created', 'modified']
        read_only_fields = ['created', 'modified', 'etudiant', 'full_name', 'type_diplome']

class DemandeSoumissionSerializer(serializers.ModelSerializer):
    # Utiliser PrimaryKeyRelatedField pour ajouter des diplômes via leurs IDs lors de la création
    diplome = serializers.PrimaryKeyRelatedField(many=True, queryset=Diploma.objects.all())

    class Meta:
        model = DemandeSoumission
        fields = ['id', 'titre', 'commentaire', 'status', 'diplome', 'year', 'created', 'modified']

    def create(self, validated_data):
        # Extraire les diplômes à partir des IDs
        diplome_data = validated_data.pop('diplome')
        demande = DemandeSoumission.objects.create(**validated_data)

        # Ajouter les diplômes à la demande via leurs IDs
        demande.diplome.set(diplome_data)

        return demande

    def to_representation(self, instance):
        """
        Modifier la représentation pour inclure les détails des diplômes et étudiants associés
        """
        # Utiliser le serializer des diplômes pour afficher leurs informations
        response = super().to_representation(instance)
        response['diplome'] = DiplomaSerializer(instance.diplome.all(), many=True).data
        return response

class DemandeSoumissionStatusSerializer(serializers.Serializer):
    key = serializers.IntegerField()
    label = serializers.CharField(max_length=50)