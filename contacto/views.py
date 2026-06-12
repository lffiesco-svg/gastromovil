from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend
import ssl
import certifi
import smtplib
import threading


def enviar_email_contacto(asunto, cuerpo, destinatario):
    try:
        backend = SMTPEmailBackend(
            host='smtp.gmail.com',
            port=587,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=True,
            use_ssl=False,
            fail_silently=False,
        )
        email = EmailMessage(
            subject=asunto,
            body=cuerpo,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[destinatario],
            connection=backend,
        )
        email.send()
        print('[DEBUG] Email enviado correctamente')
    except Exception as e:
        import traceback
        print(f'[ERROR email contacto]: {type(e).__name__}: {e}')
        traceback.print_exc()


def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        tipo = request.POST.get('tipo', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        acepta = request.POST.get('acepta')

        if not all([nombre, email, tipo, mensaje]):
            messages.error(request, 'Por favor completa todos los campos obligatorios.')
            return render(request, 'contacto/contacto.html', {'form_data': request.POST})

        if not acepta:
            messages.error(request, 'Debes aceptar la política de privacidad.')
            return render(request, 'contacto/contacto.html', {'form_data': request.POST})

        asunto = f'[GastroWeb] Consulta de {nombre} — {tipo}'
        cuerpo = f"""
Nueva consulta desde el formulario de contacto de GastroWeb:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Nombre:     {nombre}
📧 Correo:     {email}
📞 Teléfono:   {telefono or 'No indicado'}
📋 Tipo:       {tipo}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Mensaje:
{mensaje}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Este mensaje fue enviado desde gastromovil.online
        """.strip()

        hilo = threading.Thread(
            target=enviar_email_contacto,
            args=(asunto, cuerpo, settings.CONTACTO_EMAIL),
            daemon=True
        )
        hilo.start()

        messages.success(request, '¡Mensaje enviado con éxito! Te responderemos pronto.')

    return render(request, 'contacto/contacto.html')