from django.contrib import admin
from .models import Restaurante, Categoria, Producto


class CategoriaInline(admin.TabularInline):
    model = Categoria
    extra = 0
    fields = ['nombre']
    show_change_link = True


class ProductoInline(admin.TabularInline):
    model = Producto
    extra = 0
    fields = ['nombre', 'precio', 'disponible', 'imagen']


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    inlines = [CategoriaInline]
    list_display = ['id', 'nombre', 'telefono', 'activo', 'tiene_imagen']
    list_filter = ['activo']
    search_fields = ['nombre', 'direccion', 'propietario__username', 'propietario__email']
    ordering = ['-activo', 'nombre']

    fieldsets = (
        ('Información general', {
            'fields': ('propietario', 'nombre', 'direccion', 'telefono')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Imagen', {
            'fields': ('logo',)
        }),
    )

    actions = ['activar_restaurante', 'desactivar_restaurante']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(propietario=request.user)

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return obj.propietario == request.user
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return obj.propietario == request.user
        return super().has_delete_permission(request, obj)

    @admin.display(description='Tiene imagen', boolean=True)
    def tiene_imagen(self, obj):
        return bool(obj.logo)

    @admin.action(description='Activar restaurantes')
    def activar_restaurante(self, request, queryset):
        actualizados = queryset.update(activo=True)
        self.message_user(request, f'{actualizados} restaurante(s) activados')

    @admin.action(description='Desactivar restaurantes')
    def desactivar_restaurante(self, request, queryset):
        actualizados = queryset.update(activo=False)
        self.message_user(request, f'{actualizados} restaurante(s) desactivados')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    inlines = [ProductoInline]
    list_display = ['id', 'nombre', 'restaurante', 'total_productos']
    list_filter = ['restaurante']
    search_fields = ['nombre', 'restaurante__nombre']
    ordering = ['restaurante', 'nombre']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(restaurante__propietario=request.user)

    @admin.display(description='Total productos')
    def total_productos(self, obj):
        return obj.producto_set.count()


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'get_restaurante', 'categoria', 'precio', 'disponible', 'tiene_imagen']
    list_filter = ['disponible', 'categoria__restaurante']
    search_fields = ['nombre', 'descripcion', 'categoria__nombre', 'categoria__restaurante__nombre']
    ordering = ['categoria', 'nombre']

    fieldsets = (
        ('Información del producto', {
            'fields': ('categoria', 'nombre', 'descripcion')
        }),
        ('Precio y disponibilidad', {
            'fields': ('precio', 'disponible')
        }),
        ('Imagen', {
            'fields': ('imagen',)
        }),
    )

    actions = ['marcar_disponible', 'marcar_no_disponible']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(categoria__restaurante__propietario=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'categoria' and not request.user.is_superuser:
            kwargs['queryset'] = Categoria.objects.filter(restaurante__propietario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description='Restaurante')
    def get_restaurante(self, obj):
        return obj.categoria.restaurante.nombre

    @admin.display(description='Tiene imagen', boolean=True)
    def tiene_imagen(self, obj):
        return bool(obj.imagen)

    @admin.action(description='Marcar como disponible')
    def marcar_disponible(self, request, queryset):
        actualizados = queryset.update(disponible=True)
        self.message_user(request, f'{actualizados} producto(s) marcados como disponibles')

    @admin.action(description='Marcar como no disponible')
    def marcar_no_disponible(self, request, queryset):
        actualizados = queryset.update(disponible=False)
        self.message_user(request, f'{actualizados} producto(s) marcados como no disponibles')