from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Repartidor, UbicacionRepartidor
from .forms import RepartidorForm, UbicacionRepartidorForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def lista_repartidores(request):
    repartidores = Repartidor.objects.filter(activo=True).select_related('usuario')
    return render(request, 'repartidores/lista.html', {'repartidores': repartidores})


@login_required
def detalle_repartidor(request, pk):
    repartidor = get_object_or_404(Repartidor, pk=pk)
    ubicacion = UbicacionRepartidor.objects.filter(repartidor=repartidor.usuario).first()
    return render(request, 'repartidores/detalle.html', {
        'repartidor': repartidor,
        'ubicacion': ubicacion
    })


@login_required
def crear_repartidor(request):
    if request.method == 'POST':
        form = RepartidorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Repartidor creado correctamente')
            return redirect('lista_repartidores')
    else:
        form = RepartidorForm()
    return render(request, 'repartidores/form.html', {'form': form, 'accion': 'Crear repartidor'})


@login_required
def editar_repartidor(request, pk):
    repartidor = get_object_or_404(Repartidor, pk=pk)
    if request.method == 'POST':
        form = RepartidorForm(request.POST, instance=repartidor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Repartidor actualizado correctamente')
            return redirect('detalle_repartidor', pk=pk)
    else:
        form = RepartidorForm(instance=repartidor)
    return render(request, 'repartidores/form.html', {'form': form, 'accion': 'Editar repartidor'})


@login_required
def eliminar_repartidor(request, pk):
    repartidor = get_object_or_404(Repartidor, pk=pk)
    if request.method == 'POST':
        repartidor.activo = False  # Baja lógica
        repartidor.save()
        messages.success(request, 'Repartidor desactivado')
        return redirect('lista_repartidores')
    return render(request, 'repartidores/confirmar_eliminar.html', {'objeto': repartidor})


@login_required
def actualizar_ubicacion(request, pk):
    repartidor = get_object_or_404(Repartidor, pk=pk)
    ubicacion, created = UbicacionRepartidor.objects.get_or_create(repartidor=repartidor.usuario)
    if request.method == 'POST':
        form = UbicacionRepartidorForm(request.POST, instance=ubicacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ubicación actualizada')
            return redirect('detalle_repartidor', pk=pk)
    else:
        form = UbicacionRepartidorForm(instance=ubicacion)
    return render(request, 'repartidores/form.html', {'form': form, 'accion': 'Actualizar ubicación'})


@login_required
def cambiar_estado(request, pk):
    repartidor = get_object_or_404(Repartidor, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Repartidor.ESTADOS):
            repartidor.estado = nuevo_estado
            repartidor.save()
            messages.success(request, f'Estado cambiado a {nuevo_estado}')
        return redirect('detalle_repartidor', pk=pk)
    return render(request, 'repartidores/cambiar_estado.html', {'repartidor': repartidor})


@login_required
def mapa_repartidores(request):
    return render(request, 'repartidores/mapa.html')


# ── API REST ────────────────────────────────────────────────

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RepartidorSerializer, UbicacionRepartidorSerializer

@api_view(['GET'])
def api_listar_repartidores(request):
    repartidores = Repartidor.objects.all()
    serializer = RepartidorSerializer(repartidores, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def api_crear_repartidor(request):
    serializer = RepartidorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Repartidor creado', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def api_editar_repartidor(request, pk):
    try:
        repartidor = Repartidor.objects.get(pk=pk)
    except Repartidor.DoesNotExist:
        return Response({'error': 'Repartidor no encontrado'}, status=404)
    serializer = RepartidorSerializer(repartidor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Repartidor actualizado', 'data': serializer.data})
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def api_eliminar_repartidor(request, pk):
    try:
        repartidor = Repartidor.objects.get(pk=pk)
    except Repartidor.DoesNotExist:
        return Response({'error': 'Repartidor no encontrado'}, status=404)
    repartidor.delete()
    return Response({'mensaje': 'Repartidor eliminado'}, status=204)

@api_view(['POST'])
def api_crear_ubicacion(request):
    repartidor_id = request.data.get('repartidor')
    lat = request.data.get('latitud')
    lng = request.data.get('longitud')

    try:
        ubicacion, created = UbicacionRepartidor.objects.update_or_create(
            repartidor_id=repartidor_id,
            defaults={
                'latitud': lat,
                'longitud': lng
            }
        )
        return Response({
            'mensaje': 'Ubicación actualizada',
            'latitud': ubicacion.latitud,
            'longitud': ubicacion.longitud
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def api_obtener_ubicacion(request, repartidor_id):
    try:
        ubicacion = UbicacionRepartidor.objects.get(repartidor_id=repartidor_id)
        return Response({
            "latitud": ubicacion.latitud,
            "longitud": ubicacion.longitud
        })
    except UbicacionRepartidor.DoesNotExist:
        return Response({'error': 'No existe ubicación'}, status=404)

@api_view(['GET'])
def api_todas_ubicaciones(request):
    """
    Devuelve la ubicación de todos los repartidores.
    Usado por el mapa en tiempo real.
    """
    ubicaciones = UbicacionRepartidor.objects.select_related('repartidor').all()
    data = [
        {
            "repartidor_id": u.repartidor.id,
            "nombre": u.repartidor.get_full_name() or u.repartidor.username,
            "latitud": float(u.latitud),
            "longitud": float(u.longitud),
        }
        for u in ubicaciones
    ]
    return Response(data) 
# Quita el decorador temporalmente para probar
# Quita el decorador temporalmente para probar
@login_required
def compartir_ubicacion(request):
    return render(request, 'repartidores/compartir_ubicacion.html')

def seguimiento_cliente(request, repartidor_id):
    return render(request, 'repartidores/seguimiento_cliente.html', {
        'repartidor_id': repartidor_id
    })