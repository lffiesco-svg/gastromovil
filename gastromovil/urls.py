from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import redirect
from core import views
from core import views as core_views
from pedidos import views as pedidos_views
from usuarios import views as usuarios_views
from usuarios.views import logout_view
from restaurantes.views import (
    restaurante_detalle_api, restaurante_editar_api,
    productos_api, producto_crear_api, producto_eliminar_api,
    producto_editar_api, categorias_api,
    categorias_crear_api, categoria_editar_api, categoria_eliminar_api,
)
from pedidos.views import (
    pedidos_activos_api, cambiar_estado_api, listar_pedidos_api
)

urlpatterns = [
    # ── ADMIN ─────────────────────────────────────────────
    path('admin/logout/', logout_view, name='admin_logout'),
    path('admin/login/', lambda request: redirect('/usuarios/login/')),
    path('admin/', admin.site.urls),

    # ── AUTH / ALLAUTH ────────────────────────────────────
    path('accounts/', include('allauth.urls')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    # ── APPS ──────────────────────────────────────────────
    path('', views.index, name='index'),
    path('usuarios/', include('usuarios.urls')),
    path('restaurantes/', include('restaurantes.urls')),
    path('repartidores/', include('repartidores.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('carrito/', include('carrito.urls')),

    # ── PANELES ───────────────────────────────────────────
    path('panel/', views.admin_panel, name='admin_panel'),
    path('panel-repartidor/', views.panel_repartidor, name='panel_repartidor'),
    path('panel-restaurante/', views.panel_restaurante, name='panel_restaurante'),

    # ── MENÚ ──────────────────────────────────────────────
    path('menu/beer/', views.menu_beer, name='menu_beer'),
    path('menu/beer/burgers/', views.burgers, name='burgers'),
    path('menu/beer/entradas/', views.entradas, name='entradas'),
    path('menu/beer/comidas-rapidas/', views.comidas_rapidas, name='comidas_rapidas'),
    path('menu/beer/especiales/', views.especiales_beer, name='especiales_beer'),
    path('menu/beer/picadas/', views.picadas, name='picadas'),
    path('menu/beer/bebidas/', views.bebidas, name='bebidas'),
    path('menu/taqueria/', views.menu_taqueria, name='menu_taqueria'),
    path('menu/taqueria/taco-carne/', views.taco_carne, name='taco_carne'),
    path('menu/taqueria/dorilocos/', views.dorilocos, name='dorilocos'),
    path('menu/taqueria/picadas-mexicanas/', views.picadas_mexicanas, name='picadas_mexicanas'),
    path('menu/taqueria/burritos/', views.burritos, name='burritos'),
    path('menu/taqueria/maruchas/', views.maruchas, name='maruchas'),

    # ── OTRAS PÁGINAS ─────────────────────────────────────
    path('contacto/', views.contacto, name='contacto'),
    path('recuperar_contrasena/', usuarios_views.enviar_codigo_web, name='recuperar_contrasena'),
    path('mispedidos/', views.historial, name='historial'),
    path('verificar/', views.verificar_codigo, name='verificar_codigo'),
    path('verificar-registro/', usuarios_views.verificar_registro, name='verificar_registro'),
    path('enviar-codigo/', usuarios_views.enviar_codigo_web, name='enviar_codigo_web'),
    path('test-notificacion/', pedidos_views.test_notificacion, name='test_notificacion'),

    # ── API JWT ───────────────────────────────────────────
    path('api/login/', TokenObtainPairView.as_view(), name='token_login'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ── API PEDIDOS ───────────────────────────────────────
    path('api/pedidos/activos/', pedidos_activos_api, name='api_pedidos_activos'),
    path('api/pedidos/<int:pk>/estado/', cambiar_estado_api, name='api_cambiar_estado'),
    path('api/pedidos/', listar_pedidos_api, name='api_pedidos'),

    # ── API PRODUCTOS ─────────────────────────────────────
    path('api/productos/crear/', producto_crear_api, name='api_producto_crear'),
    path('api/productos/<int:pk>/eliminar/', producto_eliminar_api, name='api_producto_eliminar'),
    path('api/productos/<int:pk>/editar/', producto_editar_api, name='api_producto_editar'),
    path('api/productos/', productos_api, name='api_productos'),

    # ── API RESTAURANTES ──────────────────────────────────
    path('api/restaurantes/<int:pk>/editar/', restaurante_editar_api, name='api_restaurante_editar'),
    path('api/restaurantes/<int:pk>/', restaurante_detalle_api, name='api_restaurante_detalle'),

    # ── API CATEGORÍAS ────────────────────────────────────
    path('api/categorias/crear/', categorias_crear_api, name='api_categoria_crear'),
    path('api/categorias/<int:pk>/editar/', categoria_editar_api, name='api_categoria_editar'),
    path('api/categorias/<int:pk>/eliminar/', categoria_eliminar_api, name='api_categoria_eliminar'),
    path('api/categorias/', categorias_api, name='api_categorias'),

    # ── CHATBOT ───────────────────────────────────────────
    path('api/', include('chatbot.urls')),

    # ── RELOAD DEV ────────────────────────────────────────
    path('__reload__/', include('django_browser_reload.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()