from django.contrib import admin
from documents.models import Diploma


@admin.register(Diploma)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'diploma', 'created', 'modified')