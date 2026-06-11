from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import httpx

async def contacto(request):
    if request.method == 'POST':
        nombre  = request.POST.get('nombre', '').strip()
        email   = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        tipo    = request.POST.get('tipo', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        acepta  = request.POST.get('acepta')

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
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
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
                print(f'[DEBUG] Resend status: {response.status_code}')
                print(f'[DEBUG] Resend body:   {response.text}')

                if response.status_code in [200, 201]:
                    messages.success(request, '¡Mensaje enviado con éxito! Te responderemos pronto.')
                    return redirect('contacto')   # ← redirect limpio, evita reenvío al refrescar
                else:
                    messages.error(request, 'Hubo un error al enviar el mensaje. Intenta de nuevo.')
                    return render(request, 'contacto/contacto.html', {'form_data': request.POST})

        except Exception as e:
            import traceback
            print(f'[ERROR contacto]: {type(e).__name__}: {e}')
            traceback.print_exc()
            messages.error(request, 'Hubo un error al enviar el mensaje. Intenta de nuevo.')
            return render(request, 'contacto/contacto.html', {'form_data': request.POST})

    return render(request, 'contacto/contacto.html')