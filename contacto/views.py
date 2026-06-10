from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
import httpx


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

        try:
            with httpx.Client(timeout=15) as client:
                response = client.post(
                    "https://api.resend.com/emails",
                    headers={
                        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "from": "GastroWeb <noreply@mail.gastromovil.online>",
                        "to": [settings.CONTACTO_EMAIL],
                        "subject": asunto,
                        "text": cuerpo,
                    }
                )
                print(f'[DEBUG] Resend response: {response.status_code} {response.text}')
                if response.status_code == 200 or response.status_code == 201:
                    messages.success(request, '¡Mensaje enviado con éxito! Te responderemos pronto.')
                else:
                    print(f'[ERROR] Resend error: {response.text}')
                    messages.error(request, 'Hubo un error al enviar el mensaje. Intenta de nuevo.')
        except Exception as e:
            import traceback
            print(f'[ERROR email contacto]: {type(e).__name__}: {e}')
            traceback.print_exc()
            messages.error(request, 'Hubo un error al enviar el mensaje. Intenta de nuevo.')

    return render(request, 'contacto/contacto.html')