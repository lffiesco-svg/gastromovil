import resend

def registro(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            request.session['registro_data'] = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'telefono': form.cleaned_data['telefono'],
                'password': form.cleaned_data['password1'],
            }

            codigo = str(random.randint(100000, 999999))
            request.session['codigo_verificacion'] = codigo

            html = get_email_html(
                titulo='Código de verificación',
                contenido_central=
                    parrafo(f'Hola <strong>{form.cleaned_data["first_name"]}</strong>, gracias por registrarte en GastroWeb. Usa este código para verificar tu cuenta:') +
                    codigo_box(codigo) +
                    nota('Este código expira en 10 minutos. No lo compartas con nadie.')
            )

            resend.api_key = settings.RESEND_API_KEY
            resend.Emails.send({
                "from": "GastroWeb <noreply@gastromovil.online>",
                "to": [form.cleaned_data['email']],
                "subject": "Código de verificación - Gastroweb",
                "html": html,
            })

            return redirect('verificar_registro')
    else:
        form = UsuarioRegistroForm()
    return render(request, 'auth/register.html', {'form': form})