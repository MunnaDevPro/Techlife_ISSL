# authentication.py - CORRECTED
from django.contrib.auth.backends import ModelBackend
from accounts.models import CustomUserModel

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUserModel.objects.get(email=email)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except CustomUserModel.DoesNotExist:
            return None