import resend
import threading
from django.shortcuts import render
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

        def enviar_email():
            try:
                resend.api_key = settings.RESEND_API_KEY
                resend.Emails.send({
                    "from": "GastroWeb <noreply@gastromovil.online>",
                    "to": [settings.CONTACTO_EMAIL],
                    "subject": asunto,
                    "text": cuerpo,
                })
                print('[OK email contacto]: Enviado correctamente')
            except Exception as e:
                print(f'[ERROR email contacto]: {type(e).__name__}: {e}')

        threading.Thread(target=enviar_email, daemon=True).start()
        messages.success(request, '¡Mensaje enviado con éxito! Te responderemos pronto.')

    return render(request, 'contacto/contacto.html')