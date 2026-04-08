from django.urls import path
from . import views

urlpatterns = [
    # Vistas HTML
    path('', views.lista_repartidores, name='lista_repartidores'),
    path('<int:pk>/', views.detalle_repartidor, name='detalle_repartidor'),
    path('crear/', views.crear_repartidor, name='crear_repartidor'),
    path('<int:pk>/editar/', views.editar_repartidor, name='editar_repartidor'),
    path('<int:pk>/eliminar/', views.eliminar_repartidor, name='eliminar_repartidor'),
    path('<int:pk>/ubicacion/', views.actualizar_ubicacion, name='actualizar_ubicacion'),
    path('<int:pk>/estado/', views.cambiar_estado, name='cambiar_estado'),
    path('mapa/', views.mapa_repartidores, name='mapa_repartidores'),

    # API REST
    path('api/repartidores/', views.api_listar_repartidores),
    path('api/repartidores/crear/', views.api_crear_repartidor),
    path('api/repartidores/<int:pk>/editar/', views.api_editar_repartidor),
    path('api/repartidores/<int:pk>/eliminar/', views.api_eliminar_repartidor),
    path('api/ubicaciones/', views.api_todas_ubicaciones, name='api_todas_ubicaciones'),
    path('api/ubicaciones/crear/', views.api_crear_ubicacion),
    path('api/ubicaciones/<int:repartidor_id>/', views.api_obtener_ubicacion),
]

