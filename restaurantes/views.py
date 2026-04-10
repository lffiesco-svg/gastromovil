from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Restaurante, Categoria, Producto
from .serializers import RestauranteSerializer, CategoriaSerializer, ProductoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

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