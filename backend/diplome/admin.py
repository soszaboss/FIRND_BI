from django.contrib import admin
from diplome.models import Diploma


@admin.register(Diploma)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'diploma', 'created', 'modified')