from django.contrib import admin
from .models import Pedido, DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['precio_unitario']
    fields = ['producto', 'cantidad', 'precio_unitario']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [DetallePedidoInline]

    list_display = ['id', 'cliente', 'restaurante', 'estado', 'total', 'fecha']
    list_filter = ['estado', 'fecha', 'restaurante']
    search_fields = ['cliente__username', 'cliente__email', 'restaurante__nombre']
    readonly_fields = ['fecha', 'total']
    ordering = ['-fecha']

    fieldsets = (
        ('Información del pedido', {
            'fields': ('cliente', 'restaurante', 'direccion_entrega', 'notas')
        }),
        ('Estado y pago', {
            'fields': ('estado', 'total')
        }),
        ('Fechas', {
            'fields': ('fecha',)
        }),
    )

    # Acción para cambiar estado en masa
    actions = ['marcar_enviado', 'marcar_entregado', 'marcar_cancelado']

    @admin.action(description='Marcar como Enviado')
    def marcar_enviado(self, request, queryset):
        actualizados = queryset.exclude(estado='cancelado').update(estado='enviado')
        self.message_user(request, f'{actualizados} pedido(s) marcados como enviados')

    @admin.action(description='Marcar como Entregado')
    def marcar_entregado(self, request, queryset):
        actualizados = queryset.exclude(estado='cancelado').update(estado='entregado')
        self.message_user(request, f'{actualizados} pedido(s) marcados como entregados')

    @admin.action(description='Marcar como Cancelado')
    def marcar_cancelado(self, request, queryset):
        actualizados = queryset.update(estado='cancelado')
        self.message_user(request, f'{actualizados} pedido(s) cancelados')


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    search_fields = ['pedido__id', 'producto__nombre']
    readonly_fields = ['precio_unitario']

    def subtotal(self, obj):
        return obj.cantidad * obj.precio_unitario
    subtotal.short_description = 'Subtotal'