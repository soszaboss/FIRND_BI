from django.contrib import admin
from documents.models import Diploma, Etudiant, DemandeSoumission


@admin.register(Diploma)
class DiplomaAdmin(admin.ModelAdmin):
    list_display = ('id', 'etudiant', 'diploma', 'created', 'modified')

@admin.register(Etudiant)
class ModelNameAdmin(admin.ModelAdmin):
    pass

@admin.register(DemandeSoumission)
class ModelNameAdmin(admin.ModelAdmin):
    pass