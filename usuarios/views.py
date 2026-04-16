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

# Create your views here.

#Auth
def registro(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente! Inicia sesion.')
            return render(request, 'auth/register.html', {'form': UsuarioRegistroForm(), 'redirect_login': True})
            user = form.save ()
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect ('login')
    else:
        form = UsuarioRegistroForm()
    return render(request, 'auth/register.html', {'form': form})

import json

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
            messages.error(request, "Correo o contrasena incorrectos")
            return redirect('login')

        user = authenticate(request, username=usuario.username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            elif user.rol == 'restaurante':
                return redirect('/admin/')
            elif user.rol == 'repartidor':
                return redirect('home_repartidor')
            else:
                return redirect('index')


            return redirect('index')

        else:
            messages.error(request, "Correo o contrasena incorrectos")
            return redirect('login')

    return render(request, 'usuarios/login.html')

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
        serializer.save()
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

def enviar_codigo_web(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            usuario = Usuario.objects.get(email__iexact=email)
            
            
            CodigoRecuperacion.objects.filter(usuario=usuario).delete()

            codigo = str(secrets.SystemRandom().randint(100000, 999999))
            CodigoRecuperacion.objects.create(usuario=usuario, codigo=codigo)


            try:
                email_msg = EmailMessage(
                    subject='Código de recuperación',
                    body=f'Tu código de verificación es: {codigo}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
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