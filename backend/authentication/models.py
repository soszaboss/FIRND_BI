from django.db import models

# Create your models here.
from django.db import models

class Entreprise(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom
