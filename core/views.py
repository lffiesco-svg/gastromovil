from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from restaurantes.models import Restaurante, Categoria, Producto
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


def index(request):
    return render(request, 'index.html')

# AUTH
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('perfil')
        else:
            return render(request, 'auth/login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'auth/login.html')

def register_view(request):
    return render(request, 'auth/register.html')

@login_required(login_url='login')
def perfil(request):
    return render(request, 'usua/perfil.html')

# RESTAURANTES
def restaurantes(request):
    lista = Restaurante.objects.filter(activo=True)
    return render(request, 'restaurantes/restaurantes.html', {'restaurantes': lista})

def menu_beer(request):
    try:
        restaurante = Restaurante.objects.get(nombre__icontains='beer')
        categorias = Categoria.objects.filter(restaurante=restaurante).prefetch_related('productos')
    except Restaurante.DoesNotExist:
        categorias = []
    return render(request, 'restaurantes/menu_beer.html', {'categorias': categorias})

def menu_taqueria(request):
    try:
        restaurante = Restaurante.objects.get(nombre__icontains='taqueria')
        categorias = Categoria.objects.filter(restaurante=restaurante).prefetch_related('productos')
    except Restaurante.DoesNotExist:
        categorias = []
    return render(request, 'restaurantes/menu_taqueria.html', {'categorias': categorias})

# CATEGORIAS
def burgers(request):
    try:
        categoria = Categoria.objects.get(nombre__icontains='burger')
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
    except Categoria.DoesNotExist:
        productos = []
    return render(request, 'categorias/burgers.html', {'productos': productos})

def entradas(request):
    try:
        categoria = Categoria.objects.get(nombre__icontains='entrada')
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
    except Categoria.DoesNotExist:
        productos = []
    return render(request, 'categorias/entradas.html', {'productos': productos})

def comidas_rapidas(request):
    try:
        categoria = Categoria.objects.get(nombre__icontains='comida')
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
    except Categoria.DoesNotExist:
        productos = []
    return render(request, 'categorias/comidas_rapidas.html', {'productos': productos})

def especiales_beer(request):
    try:
        categoria = Categoria.objects.get(nombre__icontains='especial')
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
    except Categoria.DoesNotExist:
        productos = []
    return render(request, 'categorias/especiales_beer.html', {'productos': productos})

def picadas(request):
    try:
        categoria = Categoria.objects.get(nombre__icontains='picada')
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
    except Categoria.DoesNotExist:
        productos = []
    return render(request, 'categorias/picadas.html', {'productos': productos})

def bebidas(request):
    try:
        categoria = Categoria.objects.get(nombre__icontains='bebida')
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
    except Categoria.DoesNotExist:
        productos = []
    return render(request, 'categorias/bebidas.html', {'productos': productos})

def taco_carne(request):
    try:
        categoria = Categoria.objects.get(nombre__icontains='taco')
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
    except Categoria.DoesNotExist:
        productos = []
    return render(request, 'categorias/taco_carne.html', {'productos': productos})

def dorilocos(request):
    try:
        categoria = Categoria.objects.get(nombre__icontains='dori')
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
    except Categoria.DoesNotExist:
        productos = []
    return render(request, 'categorias/dorilocos.html', {'productos': productos})

def picadas_mexicanas(request):
    try:
        categoria = Categoria.objects.get(nombre__icontains='mexicana')
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
    except Categoria.DoesNotExist:
        productos = []
    return render(request, 'categorias/picadas_mexicanas.html', {'productos': productos})

def burritos(request):
    try:
        categoria = Categoria.objects.get(nombre__icontains='burrito')
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
    except Categoria.DoesNotExist:
        productos = []
    return render(request, 'categorias/burritos.html', {'productos': productos})

def maruchas(request):
    try:
        categoria = Categoria.objects.get(nombre__icontains='marucha')
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
    except Categoria.DoesNotExist:
        productos = []
    return render(request, 'categorias/maruchas.html', {'productos': productos})

def carrito(request):
    return render(request, 'pedidos/carrito.html')

def recuperar_contrasena(request):
    return render(request, 'auth/recuperar_contrasena.html')

def historial(request):
    return render(request, 'pedidos/historial.html')

def verificar_codigo(request):
    return render(request, 'auth/verificar_codigo.html')

def admin_panel(request):
    return render(request, 'paneles/superuser.html')


# ── PANEL REPARTIDOR ─────────────────────────────────────────
@login_required
def panel_repartidor(request):
    from pedidos.models import Pedido
    from django.utils import timezone
    hoy = timezone.now().date()

    # Pedidos disponibles para cualquier repartidor (estado 'enviado')
    pendientes = Pedido.objects.filter(
        estado='enviado'
    ).select_related('restaurante', 'direccion_entrega', 'cliente')

    # Pedidos que este repartidor ya aceptó y está llevando
    en_camino = Pedido.objects.filter(
        estado='en_camino',
        repartidor=request.user
    ).select_related('restaurante', 'direccion_entrega', 'cliente')

    # Pedidos que este repartidor entregó hoy
    entregados = Pedido.objects.filter(
        estado='entregado',
        repartidor=request.user,
        fecha=hoy
    ).select_related('restaurante', 'direccion_entrega', 'cliente')

    ganancias = sum(p.total for p in entregados)

    return render(request, 'paneles/panel_repartidor.html', {
        'pendientes': pendientes,
        'en_camino': en_camino,
        'entregados': entregados,
        'ganancias': ganancias,
        'repartidor_id': request.user.id,
    })
# ─────────────────────────────────────────────────────────────


def panel_restaurante(request):
    return render(request, 'paneles/panel_restaurante.html')


# ── CONTACTO ─────────────────────────────────────────────────
def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        tipo = request.POST.get('tipo', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        acepta = request.POST.get('acepta')

        if not all([nombre, email, tipo, mensaje]):
            messages.error(request, 'Por favor completa todos los campos obligatorios.')
            return render(request, 'informacion/contacto.html', {'form_data': request.POST})

        if not acepta:
            messages.error(request, 'Debes aceptar la política de privacidad.')
            return render(request, 'informacion/contacto.html', {'form_data': request.POST})

        asunto = f'[GastroWeb] Consulta de {nombre} — {tipo}'
        cuerpo = f"""
Nueva consulta desde GastroWeb:

👤 Nombre:   {nombre}
📧 Correo:   {email}
📞 Teléfono: {telefono or 'No indicado'}
📋 Tipo:     {tipo}

💬 Mensaje:
{mensaje}
        """.strip()

        try:
            send_mail(
                subject=asunto,
                message=cuerpo,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACTO_EMAIL],
                fail_silently=False,
            )
            messages.success(request, '¡Mensaje enviado con éxito! Te responderemos pronto.')
            return redirect('index')
        except Exception as e:
            print(f'[ERROR email contacto]: {e}')
            messages.error(request, 'Hubo un error al enviar el mensaje. Intenta de nuevo.')

    return render(request, 'informacion/contacto.html')