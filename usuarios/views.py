from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login , logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario, Direccion, Calificacion
from .forms import UsuarioRegistroForm, DireccionForm

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

#DIRECCIONES
@login_required
def direccion_crear(request):
    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit= False)
            direccion.usuario = request.user
            #si la direccion es principla quitar la anterior 
            if direccion.es_principal:
                Direccion.objects.filter(usuario=request.user, es_prinicpal=True).update(es_principal=False)
                direccion.save()
                messages.success(request, 'Direccion agregada.')
                return redirect('perfil')
            else:
                form=DireccionForm()
                return render(request, 'usuarios.direccion_form.html', {'form': form,'accion':'Crear'})
            
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
                form= DireccionForm(instance=direccion)
                return render(request, 'usuarios/direccion_confirmar_eliminar.html', {'direccion': direccion})

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