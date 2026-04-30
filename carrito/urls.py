from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_carrito, name='carrito'),
    path('agregar/<int:producto_id>/', views.agregar, name='carrito_agregar'),
    path('restar/<int:producto_id>/', views.restar, name='carrito_restar'),
    path('eliminar/<int:producto_id>/', views.eliminar, name='carrito_eliminar'),
    path('vaciar/', views.vaciar, name='carrito_vaciar'),
    path('confirmar/', views.confirmar_pedido, name='carrito_confirmar'),
]