
from django.contrib import admin
from django.urls import path
from core import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
