from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from pedidos import views as pedidos_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('restaurantes/', views.restaurantes, name='restaurantes'),
    path('usuarios/', include('usuarios.urls')),
    path('restaurantes/', include('restaurantes.urls')),
    path('repartidores/', include('repartidores.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('__reload__/', include('django_browser_reload.urls')),
    path('api/', include('chatbot.urls')),
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
    path('carrito/', views.carrito, name='carrito'),
    path('contacto/', views.contacto, name='contacto'), 
    path('recuperar_contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('mispedidos/', views.historial, name='historial'),
    path('verificar/', views.verificar_codigo, name='verificar_codigo'),


    path('test-notificacion/', pedidos_views.test_notificacion, name='test_notificacion'),
    path('panel/', views.admin_panel, name='admin_panel'),
    path('panel-repartidor/', views.panel_repartidor, name='panel_repartidor'),
    path('panel-restaurante/', views.panel_restaurante, name='panel_restaurante'),
 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)