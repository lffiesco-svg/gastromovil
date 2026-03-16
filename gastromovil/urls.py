
from django.contrib import admin
from django.urls import path
from core import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('restaurantes/', views.restaurantes, name='restaurantes'),
    path('usuarios/', include('usuarios.urls')),
]
