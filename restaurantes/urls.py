from django.urls import path
from . import views

urlpatterns = [
    # Restaurantes
    path('api/restaurantes/', views.listar_restaurantes),        
    path('api/restaurantes/crear/', views.crear_restaurante),    
    path('api/restaurantes/<int:pk>/', views.detalle_restaurante),
    path('api/restaurantes/<int:pk>/editar/', views.editar_restaurante),
    path('api/restaurantes/<int:pk>/eliminar/', views.eliminar_restaurante),

    # Categorias
    path('api/categorias/', views.listar_categorias),
    path('api/categorias/crear/', views.crear_categoria),
    path('api/categorias/<int:pk>/editar/', views.editar_categoria),
    path('api/categorias/<int:pk>/eliminar/', views.eliminar_categoria),

    # Productos
    path('api/productos/', views.listar_productos),
    path('api/productos/crear/', views.crear_producto),
    path('api/productos/<int:pk>/editar/', views.editar_producto),
    path('api/productos/<int:pk>/eliminar/', views.eliminar_producto),
]