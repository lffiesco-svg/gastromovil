from restaurantes.models import Producto

CART_SESSION_KEY = 'carrito'

class Carrito:
    def __init__(self, request):
        self.session = request.session
        self.carrito = self.session.get(CART_SESSION_KEY, {})

    def guardar(self):
        self.session[CART_SESSION_KEY] = self.carrito
        self.session.modified = True

    def agregar(self, producto, cantidad=1):
        pid = str(producto.id)
        if pid not in self.carrito:
            self.carrito[pid] = {
                'nombre': producto.nombre,
                'precio': str(producto.precio),
                'cantidad': 0,
                'imagen_url': producto.imagen.url if producto.imagen else None,
                'restaurante_id': producto.categoria.restaurante.id,
                'restaurante_nombre': producto.categoria.restaurante.nombre,
            }
        self.carrito[pid]['cantidad'] += cantidad
        self.guardar()

    def restaurante_id(self):
        for item in self.carrito.values():
            return item.get('restaurante_id')
        return None

    def limpiar(self):
        self.carrito = {}
        self.guardar()

    def __len__(self):
        return sum(item['cantidad'] for item in self.carrito.values())

    def total(self):
        return sum(
            float(item['precio']) * item['cantidad']
            for item in self.carrito.values()
        )

    def items(self):
        return self.carrito.values()