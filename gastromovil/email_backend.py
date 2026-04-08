import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend

class CustomSSLEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False

        context = ssl.create_default_context()
        # ✅ Mantiene verificación SSL activa
        # Solo desactiva si tu servidor usa certificado autofirmado en desarrollo
        # context.check_hostname = False
        # context.verify_mode = ssl.CERT_NONE

        self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
        self.connection.ehlo()
        self.connection.starttls(context=context)
        self.connection.ehlo()

        if self.username and self.password:
            self.connection.login(self.username, self.password)

        return True
    
    