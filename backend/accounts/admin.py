from django.contrib import admin

from accounts.models import Account


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role', 'created', 'modified', 'last_login']
    sortable_by = ('role', 'created', 'modified', 'last_login')

