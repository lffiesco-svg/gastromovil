from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        tipo = request.POST.get('tipo', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        acepta = request.POST.get('acepta')

        # Validación básica
        if not all([nombre, email, tipo, mensaje]):
            messages.error(request, 'Por favor completa todos los campos obligatorios.')
            return render(request, 'contacto/contacto.html', {
                'form_data': request.POST
            })

        if not acepta:
            messages.error(request, 'Debes aceptar la política de privacidad.')
            return render(request, 'contacto/contacto.html', {
                'form_data': request.POST
            })

        # Armar el correo
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
Este mensaje fue enviado desde gastroweb.com
        """.strip()

        try:
            send_mail(
                subject=asunto,
                message=cuerpo,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACTO_EMAIL],
                fail_silently=False,
            )
            messages.success(request, '¡Mensaje enviado con éxito! Te responderemos pronto.')
        except Exception as e:
            print(f'[ERROR email contacto]: {e}')
            messages.error(request, 'Hubo un error al enviar el mensaje. Intenta de nuevo.')

    return render(request, 'contacto/contacto.html')