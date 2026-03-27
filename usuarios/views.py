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
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

#Auth
def registro (request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            user = form.save ()
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect ('perfil')
    else:
        form = UsuarioRegistroForm()
    return render (request, 'usuarios/registro.html', {'form' : form})

@csrf_exempt      
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('perfil')
        else:
            messages.error(request, 'Usuario o contraseña incorrecta')
    return render(request, 'usuarios/login.html')
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

#PERFIL
@login_required
def perfil(request):
    direcciones = Direccion.objects.filter(usuario=request.user)
    calificaciones = Calificacion.objects.filter(cliente=request.user)
    return render(request, 'usuarios/perfil.html',{
        'usuario' : request.user,
        'direcciones' : direcciones,
        'calificaciones':calificaciones,
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
            messages.success(request, 'Dirección agregada.')
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
                Direccion.objects.filter(usuario=request.user, es_principal=True).exclude(pk=pk).update(es_principal=False)
                d.save()
                messages.success(request, 'Direccion actualizada')
                return redirect ('perfil')
            else:
                    form = DireccionForm(instance=direccion)
            return render(request, 'usuarios/direccion_form.html', {'form': form, 'accion': 'Editar'})

            
@login_required
def direccion_eliminar(request, pk):
    direccion = get_object_or_404(Direccion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        direccion.delete()
        messages.success(request, 'Dirección eliminada')
        return redirect('lista_direcciones') 
    return render(request, 'usuarios/confirmar_eliminar.html', {'objeto': direccion})

#CALIFICACIONES
@login_required
def calificacion_crear(request,pedido_id):
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
    return render(request, 'usuarios/calificacion_form.html',{'pedido': pedido})


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
        return Response({'mensaje': 'Dirección creada'}, status=201)
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

            # Buscar la dirección
            direccion = Direccion.objects.get(id=id)

            # Actualizar campos (solo si vienen en el JSON)
            direccion.calle = data.get("calle", direccion.calle)
            direccion.barrio = data.get("barrio", direccion.barrio)
            direccion.referencia = data.get("referencia", direccion.referencia)
            direccion.es_principal = data.get("es_principal", direccion.es_principal)

            direccion.save()

            return JsonResponse({
                "mensaje": "Dirección actualizada exitosamente",
                "data": {
                    "id": direccion.id,
                    "calle": direccion.calle,
                    "barrio": direccion.barrio,
                    "referencia": direccion.referencia,
                    "es_principal": direccion.es_principal
                }
            })

        except Direccion.DoesNotExist:
            return JsonResponse({
                "error": "Dirección no encontrada"
            }, status=404)

        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)
        

@csrf_exempt
def eliminar_direccion(request, id):
    if request.method == "DELETE":
        try:
            direccion = Direccion.objects.get(id=id)
            direccion.delete()

            return JsonResponse({
                "mensaje": "Dirección eliminada exitosamente"
            })

        except Direccion.DoesNotExist:
            return JsonResponse({
                "error": "Dirección no encontrada"
            }, status=404)

    return JsonResponse({"error": "Método no permitido"}, status=405)      

@csrf_exempt
def crear_calificacion(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            pedido_id = data.get("pedido")
            cliente_id = data.get("cliente")
            puntuacion = data.get("puntuacion")
            comentario = data.get("comentario", "")

            # Buscar objetos relacionados
            pedido = Pedido.objects.get(id=pedido_id)
            cliente = Usuario.objects.get(id=cliente_id)

            # Crear calificación
            calificacion = Calificacion.objects.create(
                pedido=pedido,
                cliente=cliente,
                puntuacion=puntuacion,
                comentario=comentario
            )

            return JsonResponse({
                "mensaje": "Calificación creada exitosamente",
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

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def enviar_codigo(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")

        try:
            usuario = Usuario.objects.get(email=email)

            codigo = str(random.randint(100000, 999999))

            CodigoRecuperacion.objects.create(
                usuario=usuario,
                codigo=codigo
            )

            # ENVÍO DE CORREO
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context
            send_mail(
                'Código de recuperación',
                f'Tu código es: {codigo}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return JsonResponse({
                "mensaje": "Código enviado al correo"
            })

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
                usuario=usuario,
                codigo=codigo
            ).last()

            if not registro:
                return JsonResponse({"error": "Código inválido"}, status=400)

            if registro.is_expired():
                return JsonResponse({"error": "Código expirado"}, status=400)

            usuario.set_password(nueva_password)
            usuario.save()

            registro.delete()

            return JsonResponse({
                "mensaje": "Contraseña actualizada correctamente"
            })

        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no existe"}, status=404)
        
