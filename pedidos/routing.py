from django.urls import re_path
from . import consumers
from repartidores import consumers as rep_consumers

websocket_urlpatterns = [
    re_path(
        r'ws/pedidos/(?P<tipo>\w+)/(?P<sala_id>\w+)/$',
        consumers.PedidoConsumer.as_asgi()
    ),
    re_path(
        r'ws/repartidor/(?P<repartidor_id>\w+)/$',
        rep_consumers.RepartidorConsumer.as_asgi()
    ),
]