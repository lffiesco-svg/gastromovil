from django.contrib.auth.backends import ModelBackend
from .models import Usuario

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(email=username)  # 👈 Busca por email
        except Usuario.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    