from django.urls import path
from . import views

urlpatterns = [
    #auth
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    #perfil
    path('perfil/', views.perfil, name='perfil'),

    #Direcciones
    path('direcciones/nueva/', views.direccion_crear, name='direccion_crear'),
    path('direcciones/<int:pk>/editar/', views.direccion_editar, name='direccion_editar'),
    path('direcciones/<int:pk>/eliminar/', views.direccion_elimiar, name='direccion_eliminar'),

    #calificaciones
    path('calificar/<int:pedido_id>/', views.calificacion_crear, name='calificacion_crear'),

]
