from django.db import models
from rest_framework.exceptions import ValidationError
from accounts.models import Account
from django_extensions.db.models import TimeStampedModel
import os
import uuid
import shortuuid

def diploma_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"FiRNDeBi_{instance.id}.{ext}"
    return os.path.join('diplomas/', str(instance.etudiant.id), filename)

def generate_short_uuid():
    return shortuuid.encode(uuid.uuid4())

class Model(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, unique=True, max_length=22, editable=False)

    class Meta:
        abstract = True

class Etudiant(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    phone_number = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class TypeDiplome(models.IntegerChoices):
    BTS = 1, 'BTS'
    CAP = 2, 'CAP'
    BEP = 3, 'BEP'
    BT = 4, 'BT'



class Diploma(TimeStampedModel, Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    type_diplome = models.IntegerField(choices=TypeDiplome.choices, default=TypeDiplome.BTS)
    diploma = models.FileField(upload_to=diploma_upload_path)

    @property
    def full_name(self):
        return f"{self.etudiant.first_name} {self.etudiant.last_name}"

   # @property
    #def phone_number(self):
     #   return f"{self.phone_number}"

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.id)

class DemandeSoumissionStatus(models.IntegerChoices):
    SOUMIS = 1, 'SOUMIS'
    TRAITE = 2, 'TRAITE'
    RECEPTION = 3, 'RECEPTION'
    FIN_DE_TRAITEMENT = 4, 'FIN DE TRAITEMENT'
    REJET = 5, 'REJET'

class DemandeSoumission(TimeStampedModel, models.Model):
    titre = models.CharField(max_length=120)
    commentaire = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=DemandeSoumissionStatus.choices, default=DemandeSoumissionStatus.SOUMIS)
    diplome = models.ManyToManyField(Diploma)
    year = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.pk and self.status < self.__class__.objects.get(pk=self.pk).status:
            raise ValidationError("Le statut ne peut pas être rétrogradé.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titre}"
