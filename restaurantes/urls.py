from django.urls import path
from . import views

urlpatterns = [
    #RESTAURANTES
    path('', views.lista_restaurantes, name='lista_restaurante'),
    path('<int:pk>/', views.detalle_restaurante, name='detalle_restaurante'),
    path('nuevo/', views.crear_restaurante, name='crear_restaurante'),
    path('<int:pk>/editar/', views.editar_restaurante, name='editar_restaurante'),
    path('<int:pk>/eliminar/', views.eliminar_restaurante, name='eliminar_restaurante'),

    #CATEGORIAS
    path('<int:restaurante_pk>/categoria/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categoria/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categoria/<int:pk>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),

    #PRODUCTOS
    path('categoria/<int:categoria_pk>/producto/nuevo/', views.crear_producto, name='crear_producto'),
    path('producto/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('producto/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto')
]
