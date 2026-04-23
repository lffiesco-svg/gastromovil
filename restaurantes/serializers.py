from rest_framework import serializers
from .models import Restaurante, Categoria, Producto

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    categoria_restaurante = serializers.CharField(source='categoria.restaurante.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True, read_only=True)
    class Meta:
        model = Categoria
        fields = '__all__'

class RestauranteSerializer(serializers.ModelSerializer):
    propietario_nombre = serializers.CharField(source='propietario.username', read_only=True)

    class Meta:
        model = Restaurante
        fields = '__all__'
        extra_kwargs = {
            'propietario': {'required': False},
            'nombre': {'required': False},
        }