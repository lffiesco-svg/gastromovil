from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Restaurante, Categoria, Producto
from .serializers import RestauranteSerializer, CategoriaSerializer, ProductoSerializer
from rest_framework.decorators import api_view
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
    serializer = RestauranteSerializer(restaurante, data=request.data)
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
    serializer = ProductoSerializer(producto, data=request.data)
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