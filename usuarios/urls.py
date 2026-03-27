from django.urls import path
from . import views
from .views import crear_direccion, listar_direcciones, editar_direccion, eliminar_direccion, crear_calificacion
from .views import enviar_codigo, verificar_codigo

urlpatterns = [
    #para postman 

    #crear registro
    path('api/registro/', views.registro_api),
    #crear direccion
    path('api/direcciones/crear/', crear_direccion),
    #mostrar las direcciones existentes
    path('direcciones/', listar_direcciones, name='direccion_listar'),
    #editar direccion
    path("direcciones/<int:id>/editar/", editar_direccion),
    #eliminar direccion 
    path('direcciones/<int:id>/eliminar/', eliminar_direccion), 
    #crear calificacion
    path('calificaciones/crear/', crear_calificacion),
    #enviar codigo
    path('password/enviar-codigo/', enviar_codigo),
    #verificar codigo
    path('password/verificar-codigo/', verificar_codigo),
    


    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    #perfil
    path('perfil/', views.perfil, name='perfil'),

    #Direcciones
    path('direcciones/nueva/', views.direccion_crear, name='direccion_crear'),
    path('direcciones/<int:pk>/editar/', views.direccion_editar, name='direccion_editar'),

    #calificaciones
    path('calificar/<int:pedido_id>/', views.calificacion_crear, name='calificacion_crear'),

]
