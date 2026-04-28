# carrito/context_processors.py
from .cart import Carrito

def carrito_total(request):
    carrito = Carrito(request)
    return {'carrito_total': len(carrito)}