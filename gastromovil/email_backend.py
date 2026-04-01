import ssl
from django.core.mail.backends.smtp import EmailBackend

class UnverifiedSSLEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        
        import smtplib
        self.connection = smtplib.SMTP(self.host, self.port)
        self.connection.ehlo()
        
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        self.connection.starttls(context=context)
        self.connection.ehlo()
        self.connection.login(self.username, self.password)
        return True