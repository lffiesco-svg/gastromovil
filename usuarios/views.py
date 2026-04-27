import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login , logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario, Direccion, Calificacion, CodigoRecuperacion
from .forms import UsuarioRegistroForm, DireccionForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UsuarioSerializer
from .serializers import DireccionSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotAllowed
import json
from pedidos.models import Pedido
import random 
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.core.mail import EmailMultiAlternatives
from .email_template import get_email_html, codigo_box, parrafo, nota
import threading

# Create your views here.

#Auth
@csrf_exempt
def registro(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            # ✅ No guardes todavía, guarda los datos en sesión
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

            email = EmailMultiAlternatives(
                subject='Código de verificación - Gastroweb',
                body=f'Tu código de verificación es: {codigo}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[form.cleaned_data['email']],
            )
            email.attach_alternative(html, "text/html")
            email.send(fail_silently=False)

            return redirect('verificar_registro')
    else:
        form = UsuarioRegistroForm()
    return render(request, 'auth/register.html', {'form': form})
import json

def verificar_registro(request):
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo')
        codigo_sesion = request.session.get('codigo_verificacion')
        datos = request.session.get('registro_data')

        if not datos:
            messages.error(request, 'Sesión expirada, regístrate de nuevo.')
            return redirect('registro')

        if codigo_ingresado == codigo_sesion:
            # ✅ Código válido — crea el usuario
            user = Usuario.objects.create_user(
                username=datos['email'],
                email=datos['email'],
                first_name=datos['first_name'],
                last_name=datos['last_name'],
                telefono=datos['telefono'],
                password=datos['password'],
                rol='cliente'
            )
            
            del request.session['codigo_verificacion']
            del request.session['registro_data']

            return render(request, 'auth/verificar_registro.html', {
                'verificado': True
            })
        else:
            messages.error(request, 'Código inválido. Intenta de nuevo.')

    return render(request, 'auth/verificar_registro.html')




@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Todos los campos son obligatorios")
            return redirect('login')

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, "Correo o contraseña incorrectos")
            return redirect('login')

        user = authenticate(request, username=usuario.username, password=password)

        if user is not None:
            login(request, user)

            # ── Enviar correo en segundo plano para no bloquear el redirect ──
            def enviar_correo():
                try:
                    html = get_email_html(
                        titulo='Inicio de sesión exitoso',
                        contenido_central=
                            parrafo(f'Hola <strong>{user.first_name}</strong>, has iniciado sesión exitosamente en <strong>GastroWeb</strong>.') +
                            parrafo('Si no fuiste tú, cambia tu contraseña de inmediato.') +
                            nota(f'Fecha y hora: {user.last_login.strftime("%d/%m/%Y %H:%M")} UTC')
                    )
                    email_msg = EmailMultiAlternatives(
                        subject='Inicio de sesión exitoso - Gastroweb',
                        body=f'Hola {user.first_name}, has iniciado sesión en Gastroweb.',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email],
                    )
                    email_msg.attach_alternative(html, "text/html")
                    email_msg.send(fail_silently=True)
                except Exception:
                    pass

            threading.Thread(target=enviar_correo, daemon=True).start()

            # ── Redirigir inmediatamente sin esperar el correo ──
            if user.is_superuser:
                return redirect('/admin/')
            elif user.rol == 'restaurante':
                return redirect('panel_restaurante')
            elif user.rol == 'repartidor':
                return redirect('panel_repartidor')
            else:
                return redirect('index')
        else:
            messages.error(request, "Correo o contraseña incorrectos")
            return redirect('login')

    return render(request, 'auth/login.html')

@never_cache
def logout_view(request):
    logout(request)
    request.session.flush()
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

#PERFIL
@login_required
def perfil(request):
    if request.method == 'POST':
        telefono = request.POST.get('telefono', '').strip()
        if len(telefono) > 10:
            messages.error(request, 'El telefono no puede tener mas de 10 digitos.')
            return redirect('perfil')
        usuario = request.user
        usuario.first_name = request.POST.get('first_name', usuario.first_name)
        usuario.last_name = request.POST.get('last_name', usuario.last_name)
        usuario.email = request.POST.get('email', usuario.email)
        usuario.telefono = telefono 
        usuario.save()
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfil')

    direcciones = Direccion.objects.filter(usuario=request.user)
    calificaciones = Calificacion.objects.filter(cliente=request.user)
    return render(request, 'auth/perfil.html', {
        'usuario': request.user,
        'direcciones': direcciones,
        'calificaciones': calificaciones,
    })

@login_required
def direccion_crear(request):
    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.usuario = request.user
            if direccion.es_principal:
                Direccion.objects.filter(
                    usuario=request.user, es_principal=True
                ).update(es_principal=False)
            direccion.save()
            messages.success(request, 'Direccion agregada.')
            return redirect('perfil')
    else:
        form = DireccionForm()
    return render(request, 'usuarios/direccion_form.html', {'form': form, 'accion': 'Crear'})

@login_required
def direccion_editar(request, pk):
    direccion = get_object_or_404(Direccion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = DireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            d = form.save(commit=False)
            if d.es_principal:
                Direccion.objects.filter(
                    usuario=request.user, es_principal=True
                ).exclude(pk=pk).update(es_principal=False)
            d.save()
            messages.success(request, 'Direccion actualizada')
            return redirect('perfil')
    else:
        form = DireccionForm(instance=direccion)
    return render(request, 'usuarios/direccion_form.html', {'form': form, 'accion': 'Editar'})

@login_required
def direccion_eliminar(request, pk):
    direccion = get_object_or_404(Direccion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        direccion.delete()
        messages.success(request, 'Direccion eliminada')
        return redirect('lista_direcciones')
    return render(request, 'usuarios/confirmar_eliminar.html', {'objeto': direccion})

#CALIFICACIONES
@login_required
def calificacion_crear(request, pedido_id):
    from pedidos.models import Pedido
    pedido = get_object_or_404(Pedido, pk=pedido_id, cliente=request.user)
    if hasattr(pedido, 'calificacion'):
        messages.warning(request, 'ya calificaste este pedido')
        return redirect('perfil')
    if request.method == 'POST':
        puntuacion = request.POST.get('puntuacion')
        comentario = request.POST.get('comentario', '')
        Calificacion.objects.create(
            pedido=pedido,
            cliente=request.user,
            puntuacion=puntuacion,
            comentario=comentario,
        )
        messages.success(request, 'Calificacion enviada')
        return redirect('perfil')
    return render(request, 'usuarios/calificacion_form.html', {'pedido': pedido})


#postman
@api_view(['POST'])
def registro_api(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Enviar correo de bienvenida
        send_mail(
            subject='Bienvenido a Gastroweb',
            message=f'Hola {user.username}, tu registro en Gastroweb fue exitoso. ¡Ya puedes iniciar sesión!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({'mensaje': 'Usuario creado'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def crear_direccion(request):
    serializer = DireccionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Direccion creada'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def listar_direcciones(request):
    direcciones = Direccion.objects.all()
    serializer = DireccionSerializer(direcciones, many=True)
    return Response(serializer.data)

def detalle_direccion(request, pk):
    direccion = get_object_or_404(Direccion, pk=pk)
    return render(request, 'usuarios/detalle_direccion.html', {'direccion': direccion})

@csrf_exempt
def editar_direccion(request, id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            direccion = Direccion.objects.get(id=id)
            direccion.calle = data.get("calle", direccion.calle)
            direccion.barrio = data.get("barrio", direccion.barrio)
            direccion.referencia = data.get("referencia", direccion.referencia)
            direccion.es_principal = data.get("es_principal", direccion.es_principal)
            direccion.save()
            return JsonResponse({
                "mensaje": "Direccion actualizada exitosamente",
                "data": {
                    "id": direccion.id,
                    "calle": direccion.calle,
                    "barrio": direccion.barrio,
                    "referencia": direccion.referencia,
                    "es_principal": direccion.es_principal
                }
            })
        except Direccion.DoesNotExist:
            return JsonResponse({"error": "Direccion no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Metodo no permitido"}, status=405)

@csrf_exempt
def eliminar_direccion(request, id):
    if request.method == "DELETE":
        try:
            direccion = Direccion.objects.get(id=id)
            direccion.delete()
            return JsonResponse({"mensaje": "Direccion eliminada exitosamente"})
        except Direccion.DoesNotExist:
            return JsonResponse({"error": "Direccion no encontrada"}, status=404)
    return JsonResponse({"error": "Metodo no permitido"}, status=405)

@csrf_exempt
def crear_calificacion(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            pedido_id = data.get("pedido")
            cliente_id = data.get("cliente")
            puntuacion = data.get("puntuacion")
            comentario = data.get("comentario", "")
            pedido = Pedido.objects.get(id=pedido_id)
            cliente = Usuario.objects.get(id=cliente_id)
            calificacion = Calificacion.objects.create(
                pedido=pedido,
                cliente=cliente,
                puntuacion=puntuacion,
                comentario=comentario
            )
            return JsonResponse({
                "mensaje": "Calificacion creada exitosamente",
                "data": {
                    "id": calificacion.id,
                    "pedido": pedido.id,
                    "cliente": cliente.id,
                    "puntuacion": calificacion.puntuacion,
                    "comentario": calificacion.comentario
                }
            })
        except Pedido.DoesNotExist:
            return JsonResponse({"error": "Pedido no existe"}, status=404)
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Metodo no permitido"}, status=405)


# --- RECUPERACION DE CONTRASENA (API) ---

@csrf_exempt
def enviar_codigo(request):
    if request.method == "POST":
        email = request.POST.get("email")
        print("EMAIL:", email)

        try:
            usuario = Usuario.objects.get(email=email)

            codigo = str(random.randint(100000, 999999))
            CodigoRecuperacion.objects.create(usuario=usuario, codigo=codigo)

            email_msg = EmailMessage(
                subject='Codigo de recuperacion',
                body=f'Tu codigo es: {codigo}',
                from_email='johanapalacio763@gmail.com',
                to=[email],
            )

            try:
                email_msg.send(fail_silently=False)
                print("✅ CORREO ENVIADO")
            except Exception as e:
                print("❌ ERROR SMTP:", e)
                return JsonResponse({"error": str(e)})

            return JsonResponse({"mensaje": "Codigo enviado"})

        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no existe"}, status=404)

@csrf_exempt
def verificar_codigo(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        codigo = data.get("codigo")
        nueva_password = data.get("password")
        try:
            usuario = Usuario.objects.get(email=email)
            registro = CodigoRecuperacion.objects.filter(
                usuario=usuario, codigo=codigo
            ).last()
            if not registro:
                return JsonResponse({"error": "Codigo invalido"}, status=400)
            if registro.is_expired():
                return JsonResponse({"error": "Codigo expirado"}, status=400)
            usuario.set_password(nueva_password)
            usuario.save()
            registro.delete()
            return JsonResponse({"mensaje": "Contrasena actualizada correctamente"})
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no existe"}, status=404)


# --- RECUPERACION DE CONTRASENA (WEB) ---

from django.core.mail import EmailMultiAlternatives
from .email_template import get_email_html, codigo_box, parrafo, nota

def enviar_codigo_web(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            usuario = Usuario.objects.get(email__iexact=email)
            
            CodigoRecuperacion.objects.filter(usuario=usuario).delete()
            codigo = str(secrets.SystemRandom().randint(100000, 999999))
            CodigoRecuperacion.objects.create(usuario=usuario, codigo=codigo)

            try:
                html = get_email_html(
                    titulo='Recuperación de contraseña',
                    contenido_central=
                        parrafo(f'Hola <strong>{usuario.first_name}</strong>, recibimos una solicitud para restablecer tu contraseña.') +
                        codigo_box(codigo) +
                        nota('Este código expira en 10 minutos. Si no solicitaste esto, ignora este mensaje.')
                )

                email_msg = EmailMultiAlternatives(
                    subject='Código de recuperación - Gastroweb',
                    body=f'Tu código de verificación es: {codigo}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                email_msg.attach_alternative(html, "text/html")
                email_msg.send(fail_silently=False)
                
                messages.success(request, f'Código enviado exitosamente a {email}')
                request.session['email_recuperacion'] = email
                return redirect('verificar_codigo_web')
                
            except Exception as e:
                print("ERROR REAL:", e)
                messages.error(request, f'Error real: {e}')

        except Usuario.DoesNotExist:
            messages.error(request, 'No se encontró una cuenta asociada a este correo.')
            
    return render(request, 'auth/recuperar_contrasena.html')

def verificar_codigo_web(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        codigo = request.POST.get('codigo')
        nueva_password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(email=email)

            registro = CodigoRecuperacion.objects.filter(
                usuario=usuario, codigo=codigo
            ).last()

            if not registro:
                messages.error(request, 'Codigo invalido')
                return redirect('verificar_codigo_web')
            if registro.is_expired():
                messages.error(request, 'El codigo ha expirado')
                return redirect('verificar_codigo_web')

            usuario.set_password(nueva_password)
            usuario.save()
            registro.delete()

            try:                                          
                send_mail(
                    subject='Cambio de contraseña exitoso - Gastroweb',
                    message=f'Hola {usuario.username}, tu cambio de contraseña ha sido exitoso en Gastroweb. Si no realizaste este cambio, contactanos de inmediato.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[usuario.email],
                    fail_silently=False,
                )
                print("✅ CORREO ENVIADO A:", usuario.email)
            except Exception as e:
                print("❌ ERROR AL ENVIAR CORREO:", e)

            messages.success(request, 'Contrasena actualizada correctamente')
            return redirect('login')                     

        except Usuario.DoesNotExist:                    
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'auth/verificar_codigo.html')  

@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        messages.success(request, 'Cuenta eliminada correctamente.')
        return redirect('index')
    return redirect('perfil')

@api_view(['GET'])
def listar_usuarios_api(request):
    usuarios = Usuario.objects.all().values('id', 'username', 'email', 'rol')
    return Response(list(usuarios))

@api_view(['DELETE'])
def eliminar_usuario_api(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
        usuario.delete()
        return Response({'mensaje': 'Usuario eliminado'})
    except Usuario.DoesNotExist:
        return Response({'error': 'No encontrado'}, status=404)
    
@api_view(['PUT'])
def editar_usuario_api(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
        usuario.username = request.data.get('username', usuario.username)
        usuario.email = request.data.get('email', usuario.email)
        usuario.rol = request.data.get('rol', usuario.rol)
        usuario.save()
        return Response({'mensaje': 'Usuario actualizado'})
    except Usuario.DoesNotExist:
        return Response({'error': 'No encontrado'}, status=404)