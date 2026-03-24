from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

# AUTH
def login_view(request):
    return render(request, 'auth/login.html')

def register_view(request):
    return render(request, 'auth/register.html')

def perfil(request):
    return render(request, 'auth/perfil.html')

# RESTAURANTES
def restaurantes(request):
    return render(request, 'restaurantes/restaurantes.html')

def menu_beer(request):
    return render(request, 'restaurantes/menu_beer.html')

def menu_taqueria(request):
    return render(request, 'restaurantes/menu_taqueria.html')

# CATEGORIAS
def burgers(request):
    return render(request, 'categorias/burgers.html')

def entradas(request):
    return render(request, 'categorias/entradas.html')

def comidas_rapidas(request):
    return render(request, 'categorias/comidas_rapidas.html')

def especiales_beer(request):
    return render(request, 'categorias/especiales_beer.html')

def picadas(request):
    return render(request, 'categorias/picadas.html')

def bebidas(request):
    return render(request, 'categorias/bebidas.html')

def taco_carne(request):
    return render(request, 'categorias/taco_carne.html')

def dorilocos(request):
    return render(request, 'categorias/dorilocos.html')

def picadas_mexicanas(request):
    return render(request, 'categorias/picadas_mexicanas.html')

def burritos(request):
    return render(request, 'categorias/burritos.html')

def maruchas(request):
    return render(request, 'categorias/maruchas.html')

def carrito(request):
    return render(request, 'pedidos/carrito.html')

def contacto(request):
    return render(request, 'informacion/contacto.html')

def recuperar_contrasena(request):
    return render(request, 'auth/recuperar_contrasena.html')

def historial(request):
    return render(request, 'pedidos/historial.html')