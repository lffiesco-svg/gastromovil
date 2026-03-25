from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Repartidor, UbicacionRepartidor
from .forms import RepartidorForm, UbicacionRepartidorForm

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
