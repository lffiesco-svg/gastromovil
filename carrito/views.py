import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from restaurantes.models import Producto, Restaurante
from .cart import Carrito

DOMICILIO = 3000


@login_required
@require_POST
def agregar(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito = Carrito(request)
    carrito.agregar(producto, cantidad=1)
    return JsonResponse({'ok': True, 'cantidad_total': len(carrito)})


@login_required
@require_POST
def restar(request, producto_id):
    carrito = Carrito(request)
    pid = str(producto_id)
    if pid in carrito.carrito:
        carrito.carrito[pid]['cantidad'] -= 1
        if carrito.carrito[pid]['cantidad'] <= 0:
            del carrito.carrito[pid]
        carrito.guardar()
    return JsonResponse({'ok': True, 'cantidad_total': len(carrito)})


@login_required
@require_POST
def eliminar(request, producto_id):
    carrito = Carrito(request)
    pid = str(producto_id)
    if pid in carrito.carrito:
        del carrito.carrito[pid]
        carrito.guardar()
    return JsonResponse({'ok': True, 'cantidad_total': len(carrito)})


@login_required
@require_POST
def vaciar(request):
    Carrito(request).limpiar()
    return JsonResponse({'ok': True})


@login_required
def ver_carrito(request):
    carrito = Carrito(request)

    restaurantes_dict = {}
    todos_items = []

    for pid, item in carrito.carrito.items():
        rest_id = item.get('restaurante_id')
        rest_nombre = item.get('restaurante_nombre', 'Restaurante')
        subtotal = int(float(item['precio']) * item['cantidad'])
        item_completo = {**item, 'producto_id': pid, 'subtotal': subtotal}

        todos_items.append(item_completo)

        if rest_id not in restaurantes_dict:
            restaurantes_dict[rest_id] = {
                'restaurante_id': rest_id,
                'restaurante_nombre': rest_nombre,
                'items': []
            }
        restaurantes_dict[rest_id]['items'].append(item_completo)

    restaurantes = list(restaurantes_dict.values())
    total = carrito.total()

    return render(request, 'pedidos/carrito.html', {
        'restaurantes': restaurantes,
        'items': todos_items,
        'total': int(total),
        'total_con_domicilio': int(total) + DOMICILIO if todos_items else 0,
    })


@login_required
@require_POST
def confirmar_pedido(request):
    from pedidos.models import Pedido, DetallePedido
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    carrito = Carrito(request)
    if not carrito.carrito:
        return JsonResponse({'ok': False, 'error': 'El carrito está vacío'})

    body = json.loads(request.body)
    direccion = body.get('direccion', '')
    barrio = body.get('barrio', '')
    notas = body.get('notas', '')
    metodo_pago = body.get('metodo_pago', '')

    items_por_restaurante = {}
    for pid, item in carrito.carrito.items():
        rest_id = item.get('restaurante_id')
        if rest_id not in items_por_restaurante:
            items_por_restaurante[rest_id] = []
        items_por_restaurante[rest_id].append((pid, item))

    pedidos_creados = []

    for rest_id, items in items_por_restaurante.items():
        restaurante = get_object_or_404(Restaurante, pk=rest_id)
        total_restaurante = sum(
            float(item['precio']) * item['cantidad'] for _, item in items
        )

        pedido = Pedido.objects.create(
            cliente=request.user,
            restaurante=restaurante,
            estado='pendiente',
            total=total_restaurante + DOMICILIO,
            notas=f"Dirección: {direccion}, Barrio: {barrio}. {notas} | Pago: {metodo_pago}",
        )

        for pid, item in items:
            producto = get_object_or_404(Producto, pk=int(pid))
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=item['cantidad'],
                precio_unitario=float(item['precio']),
            )

        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'restaurante_{restaurante.id}',
                {
                    'type': 'notificacion_pedido',
                    'data': {
                        'tipo': 'nuevo_pedido',
                        'mensaje': f'🍽️ ¡Nuevo pedido #{pedido.id}!',
                        'pedido_id': pedido.id,
                        'cliente': request.user.get_full_name() or request.user.username,
                        'total': str(pedido.total),
                    }
                }
            )
        except Exception:
            pass

        pedidos_creados.append(pedido.id)

    carrito.limpiar()
    return JsonResponse({'ok': True, 'pedido_id': pedidos_creados[0]})