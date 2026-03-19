from django.contrib import admin
from .models import Restaurante, Categoria, Producto


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'direccion', 'activo')
    list_filter   = ('activo',)
    search_fields = ('nombre',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'restaurante')
    list_filter   = ('restaurante',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'precio', 'categoria', 'restaurante', 'disponible')
    list_filter   = ('restaurante', 'categoria', 'disponible')
    search_fields = ('nombre', 'descripcion')