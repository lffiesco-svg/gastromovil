# repartidores/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ubicacion/(?P<repartidor_id>\d+)/$', consumers.UbicacionConsumer.as_asgi()),
]