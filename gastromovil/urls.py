
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('restaurantes/', views.restaurantes, name='restaurantes'),
    path('__reload__/', include('django_browser_reload.urls')),
    path('menu/beer/', views.menu_beer, name='menu_beer'),
    path('menu/taqueria/', views.menu_taqueria, name='menu_taqueria'),
    path('menu/beer/burgers/', views.burgers, name='burgers'),
    path('menu/beer/entradas/', views.entradas, name='entradas'),
    path('menu/beer/comidas-rapidas/', views.comidas_rapidas, name='comidas_rapidas'),
    path('menu/beer/especiales/', views.especiales_beer, name='especiales_beer'),
    path('menu/beer/picadas/', views.picadas, name='picadas'),
    path('menu/beer/bebidas/', views.bebidas, name='bebidas'),
    path('menu/taqueria/taco-carne/', views.taco_carne, name='taco_carne'),
    path('menu/taqueria/dorilocos/', views.dorilocos, name='dorilocos'),
    path('menu/taqueria/picadas-mexicanas/', views.picadas_mexicanas, name='picadas_mexicanas'),
    path('menu/taqueria/burritos/', views.burritos, name='burritos'),
    path('menu/taqueria/maruchas/', views.maruchas, name='maruchas'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('perfil/', views.perfil, name='perfil'),
]
