from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Pedido, DetallePedido
from .forms import PedidoForm, DetallePedidoForm, CambiarEstadoForm
from restaurantes.models import Producto


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

            # Procesar productos enviados desde el formulario
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

            messages.success(request, f'Pedido #{pedido.id} creado correctamente')
            return redirect('detalle_pedido', pk=pedido.pk)
    else:
        form = PedidoForm()

    # Filtrar direcciones del usuario
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


# ── Vistas para el restaurante/admin ──────────────────────────────────────────

@login_required
def pedidos_restaurante(request):
    pedidos = Pedido.objects.filter(
        restaurante__propietario=request.user
    ).select_related('cliente', 'direccion_entrega').order_by('-fecha')
    return render(request, 'pedidos/lista_restaurante.html', {'pedidos': pedidos})


@login_required
def cambiar_estado_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, restaurante__propietario=request.user)

    if request.method == 'POST':
        form = CambiarEstadoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, f'Estado actualizado a: {pedido.get_estado_display()}')
            return redirect('pedidos_restaurante')
    else:
        form = CambiarEstadoForm(instance=pedido)

    return render(request, 'pedidos/cambiar_estado.html', {
        'form': form,
        'pedido': pedido
    })