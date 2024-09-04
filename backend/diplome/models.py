from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
import os
import uuid
import shortuuid


# enregistrement du document télécharger
# puis le renomer avec le notre brand accompagné de son uuid
def diploma_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join('diplomas/', f"FiRNDeBi_{filename}")

# géneration de courte uuid
def generate_short_uuid():
    return shortuuid.encode(uuid.uuid4())


class Model(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, unique=True, max_length=22, editable=False)

    class Meta:
        abstract = True


class Diploma(TimeStampedModel, Model):
    user = models.ForeignKey(User, related_name='diplomas', on_delete=models.CASCADE)
    diploma = models.FileField(upload_to=diploma_upload_path)

    class Meta:
        ordering = ['-created']
    def __str__(self):
        return str(self.id)
