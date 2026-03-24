from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_repartidores, name='lista_repartidores'),
    path('<int:pk>/', views.detalle_repartidor, name='detalle_repartidor'),
    path('nuevo/', views.crear_repartidor, name='crear_repartidor'),
    path('<int:pk>/editar/', views.editar_repartidor, name='editar_repartidor'),
    path('<int:pk>/eliminar/', views.eliminar_repartidor, name='eliminar_repartidor'),
    path('<int:pk>/ubicacion/', views.actualizar_ubicacion, name='actualizar_ubicacion'),
    path('<int:pk>/estado/', views.cambiar_estado, name='cambiar_estado'),
]
