from django.urls import path
from . import views
from pedidos.views import test_notificacion

urlpatterns = [
    # Cliente
    path('', views.lista_pedidos, name='lista_pedidos'),
    path('<int:pk>/', views.detalle_pedido, name='detalle_pedido'),
    path('nuevo/', views.crear_pedido, name='crear_pedido'),
    path('<int:pk>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),

    # Restaurante
    path('restaurante/', views.pedidos_restaurante, name='pedidos_restaurante'),
    path('<int:pk>/estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),

    path('test-notificacion/', test_notificacion, name='test_notificacion'),
]