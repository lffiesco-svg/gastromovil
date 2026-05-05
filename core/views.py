from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from restaurantes.models import Restaurante, Categoria, Producto
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from usuarios.email_template import get_email_html, parrafo, nota

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

@login_required
def historial(request):
    from pedidos.models import Pedido
    pedidos = Pedido.objects.filter(
        cliente=request.user
    ).prefetch_related('detalles__producto').select_related(
        'restaurante', 'direccion_entrega'
    ).order_by('-fecha', '-id')
    return render(request, 'pedidos/historial.html', {'pedidos': pedidos})

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


@login_required
def panel_restaurante(request):
    try:
        restaurante = Restaurante.objects.get(propietario=request.user)
        categorias = Categoria.objects.filter(restaurante=restaurante).prefetch_related('productos')
        productos = Producto.objects.filter(categoria__restaurante=restaurante)
    except Restaurante.DoesNotExist:
        restaurante = None
        categorias = []
        productos = []
    return render(request, 'paneles/panel_restaurante.html', {
        'restaurante': restaurante,
        'categorias': categorias,
        'productos': productos,
    })

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

        try:
            html = get_email_html(
                titulo='Nueva consulta de contacto',
                contenido_central=
                    parrafo(f'Has recibido una nueva consulta desde el formulario de <strong>GastroWeb</strong>.') +
                    f"""
                    <table width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0; border-radius:10px; overflow:hidden; border:1px solid #eeeeee;">
                        <tr bgcolor="#fff5f5">
                            <td style="padding:12px 20px; font-size:13px; color:#888; font-family:Arial,sans-serif; width:130px;">👤 Nombre</td>
                            <td style="padding:12px 20px; font-size:14px; color:#333; font-family:Arial,sans-serif; font-weight:bold;">{nombre}</td>
                        </tr>
                        <tr bgcolor="#ffffff">
                            <td style="padding:12px 20px; font-size:13px; color:#888; font-family:Arial,sans-serif;">📧 Correo</td>
                            <td style="padding:12px 20px; font-size:14px; color:#333; font-family:Arial,sans-serif;">{email}</td>
                        </tr>
                        <tr bgcolor="#fff5f5">
                            <td style="padding:12px 20px; font-size:13px; color:#888; font-family:Arial,sans-serif;">📞 Teléfono</td>
                            <td style="padding:12px 20px; font-size:14px; color:#333; font-family:Arial,sans-serif;">{telefono or 'No indicado'}</td>
                        </tr>
                        <tr bgcolor="#ffffff">
                            <td style="padding:12px 20px; font-size:13px; color:#888; font-family:Arial,sans-serif;">📋 Tipo</td>
                            <td style="padding:12px 20px; font-size:14px; color:#333; font-family:Arial,sans-serif;">{tipo}</td>
                        </tr>
                        <tr bgcolor="#fff5f5">
                            <td style="padding:12px 20px; font-size:13px; color:#888; font-family:Arial,sans-serif; vertical-align:top;">💬 Mensaje</td>
                            <td style="padding:12px 20px; font-size:14px; color:#333; font-family:Arial,sans-serif; line-height:1.6;">{mensaje}</td>
                        </tr>
                    </table>
                    """ +
                    nota('Este mensaje fue enviado desde el formulario de contacto de GastroWeb.')
            )

            email_msg = EmailMultiAlternatives(
                subject=f'[GastroWeb] Consulta de {nombre} — {tipo}',
                body=f'Nueva consulta de {nombre} ({email}): {mensaje}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACTO_EMAIL],
            )
            email_msg.attach_alternative(html, "text/html")
            email_msg.send(fail_silently=False)

            messages.success(request, '¡Mensaje enviado con éxito! Te responderemos pronto.')

        except Exception as e:
            print(f'[ERROR email contacto]: {e}')
            messages.error(request, 'Hubo un error al enviar el mensaje. Intenta de nuevo.')

        return redirect('contacto')

    return render(request, 'informacion/contacto.html')