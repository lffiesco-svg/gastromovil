from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r'ws/pedidos/(?P<tipo>\w+)/(?P<sala_id>\w+)/$',
        consumers.PedidoConsumer.as_asgi()
    ),
]