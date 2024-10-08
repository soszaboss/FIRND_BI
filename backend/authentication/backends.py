from django.contrib.auth.backends import ModelBackend
from accounts.models import Account

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Account.objects.get(email=username)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None