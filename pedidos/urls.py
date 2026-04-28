from django.urls import path
from . import views
from pedidos.views import (
    lista_pedidos, detalle_pedido, crear_pedido, cancelar_pedido,
    pedidos_restaurante, cambiar_estado_pedido, test_notificacion,
    pedidos_repartidor, aceptar_entrega, marcar_entregado,
    listar_pedidos_api, pedidos_activos_api, cambiar_estado_api,
)

urlpatterns = [
    # Cliente
    path('', lista_pedidos, name='lista_pedidos'),
    path('<int:pk>/', detalle_pedido, name='detalle_pedido'),
    path('nuevo/', crear_pedido, name='crear_pedido'),
    path('<int:pk>/cancelar/', cancelar_pedido, name='cancelar_pedido'),

    # Restaurante
    path('restaurante/', pedidos_restaurante, name='pedidos_restaurante'),
    path('<int:pk>/estado/', cambiar_estado_pedido, name='cambiar_estado_pedido'),

    # Repartidor
    path('repartidor/', pedidos_repartidor, name='panel_repartidor'),
    path('<int:pk>/aceptar-entrega/', aceptar_entrega, name='aceptar_entrega'),
    path('<int:pk>/marcar-entregado/', marcar_entregado, name='marcar_entregado'),

    # Test
    path('test-notificacion/', test_notificacion, name='test_notificacion'),
]