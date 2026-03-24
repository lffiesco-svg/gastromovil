from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Restaurante, Categoria, Producto
from .forms import RestauranteForm, CategoriaForm, ProductoForm

# Create your views here.
#RESTAURANTES
def lista_restaurantes(request):
    restaurantes = Restaurante.objects.filter(activo=True)
    return render(request, 'restaurantes/lista.html', {'restaurante': restaurantes})

def detalle_restaurante(request, pk):
    restaurante = get_object_or_404(Restaurante, pk=pk, activo=True)
    categorias = Categoria.objects.filter(restaurante=restaurante).prefetch_related('productos')
    return render(request, 'restaurante/detalle.html',{
        'restaurante': restaurante,
        'caregorias' : categorias,
    })

@login_required
def crear_restaurante(request):
    if request.user.rol != 'restaurante':
        messages.error(request, 'No tienes permiso para crear restaurantes')
        return redirect('lista_restaurantes')
    if request.method == 'POST':
        form = RestauranteForm(request.POST, request.FILES)
        if form.is_valid():
            restaurante = form.save(commit=False)
            restaurante.propietario = request.user
            restaurante.save()
            messages.success(request, 'Restaurante creado')
            return redirect('detalle_restaurante', pk=restaurante.pk)
        else:
            form= RestauranteForm()
            return render(request, 'restaurantes/form.html', {'form': form, 'accion': 'Crear restaurante'})
        
@login_required
def editar_restaurante(request, pk):
    restaurante = get_object_or_404(Restaurante, pk=pk, propietario=request.user)
    if request.method == 'POST':
        form = RestauranteForm(request.POST, request.FILES, instance=restaurante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurante actualizado')
            return redirect('detalle_restaurante', pk=pk)
        else:
            form = RestauranteForm(instance=restaurante)
            return render(request, 'restaurantes/form.html', {'form': form, 'accion':'Editar Restaurante'})
        

@login_required
def eliminar_restaurante(request, pk):
    restaurante = get_object_or_404(Restaurante, pk=pk, propietario=request.user)
    if request.method == 'POST':
        restaurante.delete()
        messages.success(request, 'Restaurante eliminado')
        return redirect('lista_restaurantes')
    return render(request, 'restaurantes/confirmar_eliminar.html', {'objeto': restaurante})

#CATEGORIAS
@login_required
def crear_categoria(request, restaurante_pk):
    restaurante = get_object_or_404(Restaurante, pk=restaurante_pk, propietario=request.user)
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.restaurante = restaurante
            categoria.save()
            messages.success(request, 'categoria creada')
            return redirect('detalle_restaurante', pk=restaurante_pk)
        else:
            form=CategoriaForm()
            return render(request, 'restaurantes/form.html', {'form': form, 'accion':'crear categoria'})
        
@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, restaurante__propietario=request.user)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria actualizada')
            return redirect('detalle_restaurante', pk=categoria.restaurante.pk)
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'restaurantes/form.html', {'form': form, 'accion': 'Editar categoria'})

@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, restaurante__propietario=request.user)
    restaurante_pk = categoria.restaurante.pk
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria eliminada')
        return redirect('detalle_restaurante', pk=restaurante_pk)
    return render(request,'restaurantes/confirmar_eliminar.html', {'objeto': categoria})

# PRODUCTOS
@login_required
def crear_producto(request, categoria_pk):
    categoria = get_object_or_404(Categoria, pk=categoria_pk, restaurante__propietario=request.user)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.categoria = categoria
            producto.save()
            messages.success(request, 'Producto creado')
            return redirect('detalle_restaurante', pk=categoria.restaurante.pk)
    else:
        form = ProductoForm()  
    
    
    return render(request, 'restaurantes/form.html', {
        'form': form,
        'accion': 'Crear producto'
    })

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, categoria__restaurante__propietario=request.user)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado')
            return redirect('detalle_restaurante', pk=producto.categoria.restaurante.pk)
    else:
        form = ProductoForm(instance=producto)  
    
    
    return render(request, 'restaurantes/form.html', {
        'form': form,
        'accion': 'Editar producto'
    })

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, categoria__restaurante__propietario=request.user)
    restaurante_pk = producto.categoria.restaurante.pk
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado')
        return redirect('detalle_restaurante', pk=restaurante_pk)
    return render(request, 'restaurantes/confirmar_eliminar.html', {'objeto': producto})
