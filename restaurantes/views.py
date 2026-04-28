from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Restaurante, Categoria, Producto
from .serializers import RestauranteSerializer, CategoriaSerializer, ProductoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from better_profanity import profanity
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from pedidos.models import Pedido
from django.shortcuts import render
from usuarios.models import Calificacion


# ── RESTAURANTES ──────────────────────────────────────────
@api_view(['GET'])
def listar_restaurantes(request):
    restaurantes = Restaurante.objects.all()
    serializer = RestauranteSerializer(restaurantes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def crear_restaurante(request):
    serializer = RestauranteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Restaurante creado', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def detalle_restaurante(request, pk):
    try:
        restaurante = Restaurante.objects.get(pk=pk)
    except Restaurante.DoesNotExist:
        return Response({'error': 'Restaurante no encontrado'}, status=404)
    serializer = RestauranteSerializer(restaurante)
    return Response(serializer.data)

@api_view(['PUT'])
def editar_restaurante(request, pk):
    try:
        restaurante = Restaurante.objects.get(pk=pk)
    except Restaurante.DoesNotExist:
        return Response({'error': 'Restaurante no encontrado'}, status=404)
    
    # partial=True permite enviar solo los campos que quieres cambiar
    serializer = RestauranteSerializer(restaurante, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Restaurante actualizado', 'data': serializer.data})
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def eliminar_restaurante(request, pk):
    try:
        restaurante = Restaurante.objects.get(pk=pk)
    except Restaurante.DoesNotExist:
        return Response({'error': 'Restaurante no encontrado'}, status=404)
    restaurante.delete()
    return Response({'mensaje': 'Restaurante eliminado'}, status=204)


# ── CATEGORIAS ────────────────────────────────────────────
@api_view(['GET'])
def listar_categorias(request):
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def crear_categoria(request):
    serializer = CategoriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Categoría creada', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def editar_categoria(request, pk):
    try:
        categoria = Categoria.objects.get(pk=pk)
    except Categoria.DoesNotExist:
        return Response({'error': 'Categoría no encontrada'}, status=404)
    serializer = CategoriaSerializer(categoria, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Categoría actualizada', 'data': serializer.data})
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def eliminar_categoria(request, pk):
    try:
        categoria = Categoria.objects.get(pk=pk)
    except Categoria.DoesNotExist:
        return Response({'error': 'Categoría no encontrada'}, status=404)
    categoria.delete()
    return Response({'mensaje': 'Categoría eliminada'}, status=204)


# ── PRODUCTOS ─────────────────────────────────────────────
@api_view(['GET'])
def listar_productos(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def crear_producto(request):
    serializer = ProductoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Producto creado', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def editar_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    
    serializer = ProductoSerializer(producto, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Producto actualizado', 'data': serializer.data})
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def eliminar_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    producto.delete()
    return Response({'mensaje': 'Producto eliminado'}, status=204)


#no permitir groserias en los comentarios
PALABRAS_GROSERAS = [
    "mierda", "puta", "puto", "idiota", "imbecil", "estupido", "estupida",
    "pendejo", "pendeja", "cabron", "cabrona", "hijueputa", "malparido",
    "malparida", "gonorrea", "hp", "marica", "güevon", "huevon", "culero",
    "chingada", "chingar", "verga", "coño", "joder", "gilipollas", "capullo",
    "cacorro", "zorra", "zorro", "cerdo", "cerda", "cabrón", "cabróna", "pichula",
    "zungaa", "chingada madre", "chingada tu madre", "chingada su madre", "chingada la madre",
    "pendeja madre", "pendejo madre", "hijueputa madre", "malparido madre", "malparida madre",
    "care culo", "vete a la mierda", "vete a la chingada", "vete a la verga", "vete al carajo",
    "mamaguevo", "monda", "care monda", "sopla monda", "maricon", 
] 
profanity.add_censor_words(PALABRAS_GROSERAS)

@login_required
def calificar_restaurante(request, pk):
    from django.contrib import messages
    restaurante = get_object_or_404(Restaurante, pk=pk)
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        puntuacion = request.POST.get('puntuacion')
        comentario = request.POST.get('comentario', '')

        if profanity.contains_profanity(comentario):
            messages.error(request, 'Tu comentario contiene palabras inapropiadas. Por favor, edítalo.')
            return redirect('pagina_restaurante', pk=pk)

        pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
        if not hasattr(pedido, 'calificacion'):
            Calificacion.objects.create(
                pedido=pedido,
                cliente=request.user,
                puntuacion=puntuacion,
                comentario=comentario
            )
    return redirect('pagina_restaurante', pk=pk)

def pagina_restaurante(request, pk):
    restaurante = get_object_or_404(Restaurante, pk=pk)
    categorias = Categoria.objects.filter(restaurante=restaurante)
    calificaciones = Calificacion.objects.filter(pedido__restaurante=restaurante)
    promedio = round(sum(c.puntuacion for c in calificaciones) / calificaciones.count(), 1) if calificaciones.count() > 0 else None

    puede_calificar = False
    pedido_para_calificar = None
    if request.user.is_authenticated:
        pedido_para_calificar = Pedido.objects.filter(
            cliente=request.user,
            restaurante=restaurante,
            estado='entregado'
        ).exclude(calificacion__isnull=False).first()
        puede_calificar = pedido_para_calificar is not None

    return render(request, 'restaurante_detalle.html', {
        'restaurante': restaurante,
        'categorias': categorias,
        'calificaciones': calificaciones,
        'promedio': promedio,
        'puede_calificar': puede_calificar,
        'pedido_para_calificar': pedido_para_calificar,
    })


def vista_restaurantes(request):
    """Vista HTML para mostrar la lista de restaurantes activos."""
    restaurantes = Restaurante.objects.filter(activo=True)
    return render(request, 'restaurantes/restaurantes.html', {
        'restaurantes': restaurantes,
    })

@login_required
def panel_restaurante(request):
    try:
        restaurante = request.user.restaurante
    except Restaurante.DoesNotExist:
        restaurante = None
    return render(request, 'paneles/panel_restaurante.html', {'restaurante': restaurante})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restaurante_detalle_api(request, pk):
    r = get_object_or_404(Restaurante, pk=pk, propietario=request.user)
    return Response({
        'id': r.id,
        'nombre': r.nombre,
        'direccion': r.direccion,
        'telefono': r.telefono,
        'activo': r.activo,
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def restaurante_editar_api(request, pk):
    r = get_object_or_404(Restaurante, pk=pk, propietario=request.user)
    r.nombre = request.data.get('nombre', r.nombre)
    r.direccion = request.data.get('direccion', r.direccion)
    r.telefono = request.data.get('telefono', r.telefono)
    r.activo = request.data.get('activo', r.activo)
    r.save()
    return Response({'mensaje': 'Guardado correctamente'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def productos_api(request):
    productos = Producto.objects.filter(
        categoria__restaurante__propietario=request.user
    ).select_related('categoria', 'categoria__restaurante')
    data = [{
        'id': p.id,
        'nombre': p.nombre,
        'precio': str(p.precio),
        'descripcion': p.descripcion,
        'disponible': p.disponible,
        'imagen': request.build_absolute_uri(p.imagen.url) if p.imagen else None,
        'categoria_nombre': p.categoria.nombre if p.categoria else '-',
        'categoria_id': p.categoria_id,
        'categoria_restaurante_id': p.categoria.restaurante_id if p.categoria else None,
    } for p in productos]
    return Response(data)

    data = [{
        'id': p.id,
        'nombre': p.nombre,
        'precio': str(p.precio),
        'descripcion': p.descripcion,
        'disponible': p.disponible,
        'imagen': request.build_absolute_uri(p.imagen.url) if p.imagen else None,
        'categoria_nombre': p.categoria.nombre if p.categoria else '-',
        'categoria_restaurante_id': p.restaurante_id,  # directo, sin pasar por categoria
    } for p in productos]
    return Response(data)


from decimal import Decimal, InvalidOperation

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def producto_crear_api(request):
    nombre = request.data.get('nombre', '').strip()
    precio = request.data.get('precio')
    descripcion = request.data.get('descripcion', '')
    disponible = request.data.get('disponible', 'true') in [True, 'true', 'True']
    categoria_id = request.data.get('categoria')
    imagen = request.FILES.get('imagen')

    if not nombre or not precio:
        return Response({'error': 'Nombre y precio son obligatorios'}, status=400)

    try:
        precio = Decimal(precio)
    except (InvalidOperation, TypeError):
        return Response({'error': 'Precio inválido'}, status=400)

    restaurante = get_object_or_404(Restaurante, propietario=request.user)

    categoria = None
    if categoria_id and str(categoria_id).strip():
        categoria = get_object_or_404(Categoria, pk=categoria_id, restaurante=restaurante)

    producto = Producto.objects.create(
        nombre=nombre,
        precio=precio,
        descripcion=descripcion,
        disponible=disponible,
        categoria=categoria,
    )

    if imagen:
        producto.imagen = imagen
        producto.save()

    return Response({'mensaje': 'Producto creado', 'id': producto.id})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def producto_eliminar_api(request, pk):
    # Validar que el producto es del restaurante del usuario
    producto = get_object_or_404(Producto, pk=pk, categoria__restaurante__propietario=request.user)
    producto.delete()
    return Response({'mensaje': 'Eliminado'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def categorias_api(request):
    categorias = Categoria.objects.filter(restaurante__propietario=request.user)
    data = [{'id': c.id, 'nombre': c.nombre, 'restaurante': c.restaurante_id} for c in categorias]
    return Response(data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def producto_editar_api(request, pk):
    producto = get_object_or_404(
    Producto,
    pk=pk,
    categoria__restaurante__propietario=request.user
)
    producto.nombre = request.data.get('nombre', producto.nombre)
    producto.precio = request.data.get('precio', producto.precio)
    producto.descripcion = request.data.get('descripcion', producto.descripcion)
    producto.disponible = request.data.get('disponible', producto.disponible)
    categoria_id = request.data.get('categoria')
    if categoria_id:
        restaurante = get_object_or_404(Restaurante, propietario=request.user)
        producto.categoria = get_object_or_404(Categoria, pk=categoria_id, restaurante=restaurante)
    if request.FILES.get('imagen'):
        producto.imagen = request.FILES.get('imagen')
    producto.save()
    return Response({'mensaje': 'Producto actualizado'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def categorias_crear_api(request):
    restaurante = get_object_or_404(Restaurante, propietario=request.user)
    nombre = request.data.get('nombre', '').strip()
    if not nombre:
        return Response({'error': 'Nombre requerido'}, status=400)
    c = Categoria.objects.create(nombre=nombre, restaurante=restaurante)
    return Response({'mensaje': 'Categoría creada', 'id': c.id})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def categoria_editar_api(request, pk):
    restaurante = get_object_or_404(Restaurante, propietario=request.user)
    c = get_object_or_404(Categoria, pk=pk, restaurante=restaurante)
    c.nombre = request.data.get('nombre', c.nombre)
    c.save()
    return Response({'mensaje': 'Categoría actualizada'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def categoria_eliminar_api(request, pk):
    restaurante = get_object_or_404(Restaurante, propietario=request.user)
    c = get_object_or_404(Categoria, pk=pk, restaurante=restaurante)
    c.delete()
    return Response({'mensaje': 'Eliminada'})