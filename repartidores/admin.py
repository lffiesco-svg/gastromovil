from django.contrib import admin
from .models import Repartidor, UbicacionRepartidor


@admin.register(Repartidor)
class RepartidorAdmin(admin.ModelAdmin):
    list_display = ['get_nombre', 'get_email', 'activo']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'usuario__email']
    list_filter = ['activo']
    actions = ['marcar_disponible', 'marcar_inactivo', 'activar_repartidor', 'desactivar_repartidor']

    @admin.display(description='Nombre completo')
    def get_nombre(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.usuario.email

    @admin.action(description='Marcar como Disponible')
    def marcar_disponible(self, request, queryset):
        actualizados = queryset.filter(activo=True).update(estado='disponible')
        self.message_user(request, f'{actualizados} repartidor(es) marcados como disponibles')

    @admin.action(description='Marcar como Inactivo')
    def marcar_inactivo(self, request, queryset):
        actualizados = queryset.update(estado='inactivo')
        self.message_user(request, f'{actualizados} repartidor(es) marcados como inactivos')

    @admin.action(description='Activar repartidores')
    def activar_repartidor(self, request, queryset):
        actualizados = queryset.update(activo=True)
        self.message_user(request, f'{actualizados} repartidor(es) activados')

    @admin.action(description='Desactivar repartidores')
    def desactivar_repartidor(self, request, queryset):
        actualizados = queryset.update(activo=False, estado='inactivo')
        self.message_user(request, f'{actualizados} repartidor(es) desactivados')


@admin.register(UbicacionRepartidor)
class UbicacionRepartidorAdmin(admin.ModelAdmin):
    list_display = ['get_repartidor', 'latitud', 'longitud', 'actualizado']
    search_fields = ['repartidor__usuario__username', 'repartidor__usuario__first_name']
    readonly_fields = ['actualizado']
    ordering = ['-actualizado']

    @admin.display(description='Repartidor')
    def get_repartidor(self, obj):
        return obj.repartidor.usuario.get_full_name() or obj.repartidor.usuario.username