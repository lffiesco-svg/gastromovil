from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Direccion, Calificacion


class DireccionInline(admin.TabularInline):
    model = Direccion
    extra = 0
    fields = ['calle', 'barrio', 'referencia', 'es_principal']


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    inlines = [DireccionInline]

    list_display = ['id', 'username', 'get_nombre_completo', 'email', 'rol', 'telefono', 'is_active']
    list_filter = ['rol', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'telefono']
    ordering = ['username']

    # Extiende los fieldsets de UserAdmin con los campos personalizados
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('telefono', 'rol')
        }),
    )

    # Para el formulario de creación de usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('telefono', 'rol')
        }),
    )

    actions = ['activar_usuarios', 'desactivar_usuarios',
                'marcar_como_cliente', 'marcar_como_repartidor', 'marcar_como_restaurante']

    @admin.display(description='Nombre completo')
    def get_nombre_completo(self, obj):
        return obj.get_full_name() or '—'

    @admin.action(description='Activar usuarios')
    def activar_usuarios(self, request, queryset):
        actualizados = queryset.update(is_active=True)
        self.message_user(request, f'{actualizados} usuario(s) activados')

    @admin.action(description='Desactivar usuarios')
    def desactivar_usuarios(self, request, queryset):
        actualizados = queryset.exclude(is_superuser=True).update(is_active=False)
        self.message_user(request, f'{actualizados} usuario(s) desactivados')

    @admin.action(description='Cambiar rol a Cliente')
    def marcar_como_cliente(self, request, queryset):
        actualizados = queryset.update(rol='cliente')
        self.message_user(request, f'{actualizados} usuario(s) cambiados a cliente')

    @admin.action(description='Cambiar rol a Repartidor')
    def marcar_como_repartidor(self, request, queryset):
        actualizados = queryset.update(rol='repartidor')
        self.message_user(request, f'{actualizados} usuario(s) cambiados a repartidor')

    @admin.action(description='Cambiar rol a Restaurante')
    def marcar_como_restaurante(self, request, queryset):
        actualizados = queryset.update(rol='restautante')  # Respeta el typo del modelo
        self.message_user(request, f'{actualizados} usuario(s) cambiados a restaurante')


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'calle', 'barrio', 'es_principal']
    list_filter = ['es_principal', 'barrio']
    search_fields = ['usuario__username', 'calle', 'barrio']
    ordering = ['usuario', '-es_principal']

    actions = ['marcar_principal']

    @admin.action(description='Marcar como dirección principal')
    def marcar_principal(self, request, queryset):
        for direccion in queryset:
            # Desactiva las demás direcciones del mismo usuario
            Direccion.objects.filter(usuario=direccion.usuario).update(es_principal=False)
            direccion.es_principal = True
            direccion.save()
        self.message_user(request, f'{queryset.count()} dirección(es) marcadas como principales')


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'get_restaurante', 'puntuacion', 'fecha', 'tiene_comentario']
    list_filter = ['puntuacion', 'fecha']
    search_fields = ['cliente__username', 'pedido__id', 'comentario']
    readonly_fields = ['fecha', 'pedido', 'cliente', 'puntuacion']
    ordering = ['-fecha']

    fieldsets = (
        ('Información', {
            'fields': ('pedido', 'cliente', 'puntuacion')
        }),
        ('Comentario', {
            'fields': ('comentario',)
        }),
        ('Fecha', {
            'fields': ('fecha',)
        }),
    )

    @admin.display(description='Restaurante')
    def get_restaurante(self, obj):
        return obj.pedido.restaurante.nombre

    @admin.display(description='Tiene comentario', boolean=True)
    def tiene_comentario(self, obj):
        return bool(obj.comentario)
