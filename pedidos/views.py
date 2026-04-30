from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Pedido, DetallePedido
from .forms import PedidoForm, DetallePedidoForm, CambiarEstadoForm
from restaurantes.models import Producto, Restaurante
# Vista temporal de prueba
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from .models import Pedido

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(
        cliente=request.user
    ).select_related('restaurante', 'direccion_entrega').order_by('-fecha')
    return render(request, 'pedidos/lista.html', {'pedidos': pedidos})


@login_required
def detalle_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, cliente=request.user)
    detalles = pedido.detalles.select_related('producto').all()
    return render(request, 'pedidos/detalle.html', {
        'pedido': pedido,
        'detalles': detalles
    })


@login_required
@transaction.atomic
def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = request.user
            pedido.save()

            productos_ids = request.POST.getlist('producto')
            cantidades = request.POST.getlist('cantidad')
            total = 0

            for producto_id, cantidad in zip(productos_ids, cantidades):
                cantidad = int(cantidad)
                if cantidad > 0:
                    producto = get_object_or_404(Producto, pk=producto_id)
                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio
                    )
                    total += producto.precio * cantidad

            pedido.total = total
            pedido.save()

            # ── NOTIFICAR AL RESTAURANTE ──────────────────
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'restaurante_{pedido.restaurante.id}',
                {
                    'type': 'notificacion_pedido',
                    'data': {
                        'tipo': 'nuevo_pedido',
                        'mensaje': f'🍽️ ¡Nuevo pedido #{pedido.id}!',
                        'pedido_id': pedido.id,
                        'cliente': request.user.get_full_name() or request.user.username,
                        'total': str(pedido.total),
                        'notas': pedido.notas,
                    }
                }
            )
            # ─────────────────────────────────────────────

            messages.success(request, f'Pedido #{pedido.id} creado correctamente')
            return redirect('detalle_pedido', pk=pedido.pk)
    else:
        form = PedidoForm()

    form.fields['direccion_entrega'].queryset = form.fields[
        'direccion_entrega'].queryset.filter(usuario=request.user)

    return render(request, 'pedidos/form.html', {'form': form, 'accion': 'Crear pedido'})


@login_required
def cancelar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, cliente=request.user)

    if pedido.estado not in ['pendiente', 'aceptado']:
        messages.error(request, 'Este pedido ya no puede cancelarse')
        return redirect('detalle_pedido', pk=pk)

    if request.method == 'POST':
        pedido.estado = 'cancelado'
        pedido.save()
        messages.success(request, f'Pedido #{pedido.id} cancelado')
        return redirect('lista_pedidos')

    return render(request, 'pedidos/confirmar_cancelar.html', {'pedido': pedido})


@login_required
def pedidos_restaurante(request):
    restaurante = get_object_or_404(Restaurante, propietario=request.user)
    pedidos = Pedido.objects.filter(
        restaurante=restaurante
    ).select_related('cliente', 'direccion_entrega').order_by('-fecha')
    
    return render(request, 'pedidos/lista_restaurante.html', {
        'pedidos': pedidos,
        'restaurante': restaurante,  # <- esto faltaba
    })


@login_required
def cambiar_estado_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, restaurante__propietario=request.user)

    if request.method == 'POST':
        form = CambiarEstadoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()

            channel_layer = get_channel_layer()

            # ── SI EL ESTADO ES "enviado" → NOTIFICAR AL REPARTIDOR ──
            if pedido.estado == 'enviado':
                # Buscar repartidor disponible
                from repartidores.models import Repartidor
                repartidor = Repartidor.objects.filter(
                    estado='disponible', activo=True
                ).first()

                if repartidor:
                    async_to_sync(channel_layer.group_send)(
                        f'repartidor_{repartidor.id}',
                        {
                            'type': 'notificacion_pedido',
                            'data': {
                                'tipo': 'pedido_listo',
                                'mensaje': f'🛵 ¡Pedido #{pedido.id} listo para recoger!',
                                'pedido_id': pedido.id,
                                'restaurante': pedido.restaurante.nombre,
                                'direccion_restaurante': pedido.restaurante.direccion,
                                'direccion_entrega': str(pedido.direccion_entrega),
                            }
                        }
                    )

            # ── NOTIFICAR AL CLIENTE DEL CAMBIO DE ESTADO ────────────
            async_to_sync(channel_layer.group_send)(
                f'cliente_{pedido.cliente.id}',
                {
                    'type': 'notificacion_pedido',
                    'data': {
                        'tipo': 'cambio_estado',
                        'mensaje': f'📦 Tu pedido #{pedido.id} está: {pedido.get_estado_display()}',
                        'pedido_id': pedido.id,
                        'estado': pedido.estado,
                    }
                }
            )
            # ─────────────────────────────────────────────────────────

            messages.success(request, f'Estado actualizado a: {pedido.get_estado_display()}')
            return redirect('pedidos_restaurante')
    else:
        form = CambiarEstadoForm(instance=pedido)

    return render(request, 'pedidos/cambiar_estado.html', {
        'form': form,
        'pedido': pedido
    })

def test_notificacion(request):
    tipo = request.GET.get('tipo', 'restaurante')
    sala = request.GET.get('sala', '1')
    mensaje = request.GET.get('mensaje', 'Notificación de prueba')

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{tipo}_{sala}",
        {
            "type": "notificacion_pedido",
            "data": {
                "mensaje": mensaje,
                "pedido_id": 42,
            }
        }
    )
    return JsonResponse({"ok": True, "enviado_a": f"{tipo}_{sala}"})

@login_required
def pedidos_repartidor(request):
    from django.utils import timezone
    hoy = timezone.now().date()
    
    pendientes = Pedido.objects.filter(
        estado='enviado'
    ).select_related('restaurante', 'direccion_entrega', 'cliente')
    
    en_camino = Pedido.objects.filter(
        estado='en_camino',
        repartidor=request.user
    ).select_related('restaurante', 'direccion_entrega', 'cliente')
    
    entregados = Pedido.objects.filter(
        estado='entregado',
        repartidor=request.user,
        fecha=hoy
    ).select_related('restaurante', 'direccion_entrega', 'cliente')
    
    return render(request, 'pedidos/panel_repartidor.html', {
        'pendientes': pendientes,
        'en_camino': en_camino,
        'entregados': entregados,
    })

@login_required
def aceptar_entrega(request, pk):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, pk=pk, estado='enviado')
        pedido.estado = 'en_camino'
        pedido.repartidor = request.user
        pedido.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)

@login_required
def marcar_entregado(request, pk):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, pk=pk, estado='en_camino', repartidor=request.user)
        pedido.estado = 'entregado'
        pedido.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_pedidos_api(request):
    pedidos = Pedido.objects.filter(
        restaurante__propietario=request.user
    ).select_related('cliente', 'restaurante', 'direccion_entrega').order_by('-fecha')
    
    data = [{
        'id': p.id,
        'cliente_nombre': p.cliente.get_full_name() or p.cliente.username,
        'total': str(p.total),
        'estado': p.estado,
        'fecha': p.fecha.isoformat(),
        'notas': p.notas,
        'direccion': str(p.direccion_entrega) if p.direccion_entrega else '',
        'productos': [{
            'nombre': d.producto.nombre,
            'cantidad': d.cantidad,
            'precio': str(d.precio_unitario),
        } for d in p.detalles.select_related('producto').all()]
    } for p in pedidos]
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pedidos_activos_api(request):
    pedidos = Pedido.objects.filter(
        restaurante__propietario=request.user,
        estado__in=['pendiente', 'aceptado', 'preparando']
    ).select_related('cliente', 'direccion_entrega').prefetch_related('detalles__producto').order_by('-fecha')

    data = [{
        'id': p.id,
        'cliente': p.cliente.get_full_name() or p.cliente.username,
        'total': str(p.total),
        'estado': p.estado,
        'direccion': str(p.direccion_entrega) if p.direccion_entrega else 'Sin dirección',
        'notas': p.notas,
        'productos': [{
            'nombre': d.producto.nombre,
            'cantidad': d.cantidad,
        } for d in p.detalles.all()]
    } for p in pedidos]
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cambiar_estado_api(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, restaurante__propietario=request.user)
    nuevo_estado = request.data.get('estado')

    estados_validos = [e[0] for e in Pedido.ESTADOS]
    if nuevo_estado not in estados_validos:
        return Response({'error': 'Estado inválido'}, status=400)

    pedido.estado = nuevo_estado
    pedido.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'cliente_{pedido.cliente.id}',
        {
            'type': 'notificacion_pedido',
            'data': {
                'tipo': 'cambio_estado',
                'mensaje': f'Tu pedido #{pedido.id} está: {pedido.get_estado_display()}',
                'pedido_id': pedido.id,
                'estado': pedido.estado,
            }
        }
    )
    return Response({'mensaje': f'Estado actualizado a {pedido.get_estado_display()}'})