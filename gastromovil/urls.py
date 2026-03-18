
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('restaurantes/', views.restaurantes, name='restaurantes'),
    path('__reload__/', include('django_browser_reload.urls')),
    path('api/', include('chatbot.urls')),
]
