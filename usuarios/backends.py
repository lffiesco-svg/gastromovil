from django.contrib.auth.backends import ModelBackend
from .models import Usuario
import ssl
import certifi
import smtplib
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(email=username)  # 👈 Busca por email
        except Usuario.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    

class SSLEmailBackend(SMTPEmailBackend):
    def open(self):
        if self.connection:
            return False
        try:
            self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            self.connection.ehlo()
            if self.use_tls:
                ctx = ssl.create_default_context(cafile=certifi.where())
                self.connection.starttls(context=ctx)
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise
            return False

    def close(self):
        if self.connection is None:
            return
        try:
            self.connection.quit()
        except Exception:
            pass
        finally:
            self.connection = None