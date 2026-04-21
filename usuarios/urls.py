from django.urls import path
from . import views
from .views import crear_direccion, listar_direcciones, editar_direccion, eliminar_direccion, crear_calificacion
from .views import enviar_codigo, verificar_codigo, verificar_codigo_web, enviar_codigo_web, eliminar_cuenta

urlpatterns = [
    # API para Postman
    path('api/registro/', views.registro_api),
    path('registro/', views.registro, name='registro_web'),
    #crear direccion
    path('api/direcciones/crear/', crear_direccion),
    path('api/direcciones/', listar_direcciones, name='direccion_listar'),
    path('api/direcciones/<int:id>/editar/', editar_direccion),
    path('api/direcciones/<int:id>/eliminar/', eliminar_direccion),
    path('api/calificaciones/crear/', crear_calificacion),
    path('api/password/enviar-codigo/', enviar_codigo),
    path('api/password/verificar-codigo/', verificar_codigo),

    # Web
    path('registro/', views.registro, name='registro'),  
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('eliminar-cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),

    # Perfil
    path('perfil/', views.perfil, name='perfil'),


    # Direcciones
    path('direcciones/nueva/', views.direccion_crear, name='direccion_crear'),
    path('direcciones/<int:pk>/editar/', views.direccion_editar, name='direccion_editar'),
    path('direcciones/<int:pk>/eliminar/', views.direccion_eliminar, name='direccion_eliminar'),  

    # Calificaciones
    path('calificar/<int:pedido_id>/', views.calificacion_crear, name='calificacion_crear'),

    path('recuperar/', views.enviar_codigo_web, name='enviar_codigo_web'),
    path('verificar-codigo/', views.verificar_codigo_web, name='verificar_codigo_web'),
    path('verificar-registro/', views.verificar_registro, name='verificar_registro'),

    path('api/usuarios/', views.listar_usuarios_api),
    path('api/usuarios/<int:pk>/eliminar/', views.eliminar_usuario_api),

]
