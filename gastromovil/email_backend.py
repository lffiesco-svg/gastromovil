import ssl
import certifi
import smtplib
from django.core.mail.backends.smtp import EmailBackend

class UnverifiedSSLEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            self.connection = smtplib.SMTP(
                self.host, self.port, timeout=self.timeout
            )
            self.connection.ehlo()
            if self.use_tls:
                self.connection.starttls(context=context)
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise