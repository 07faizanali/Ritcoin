from django.contrib.auth.backends import BaseBackend
from .models import ZqUser

class ZqUserEmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        try:
            user = ZqUser.objects.get(email=email)
        except ZqUser.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return ZqUser.objects.get(pk=user_id)
        except ZqUser.DoesNotExist:
            return None
