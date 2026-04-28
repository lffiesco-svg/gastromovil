# repartidores/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # El que ya tenías
    re_path(r'ws/ubicacion/(?P<repartidor_id>\d+)/$', consumers.UbicacionConsumer.as_asgi()),
    # NUEVO
    re_path(r'ws/repartidor/(?P<repartidor_id>\d+)/$', consumers.RepartidorConsumer.as_asgi()),
]