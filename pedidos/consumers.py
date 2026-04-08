import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PedidoConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.tipo = self.scope['url_route']['kwargs']['tipo']
        self.sala_id = self.scope['url_route']['kwargs']['sala_id']
        self.group_name = f"{self.tipo}_{self.sala_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print(f"✅ Conectado: {self.group_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Este método se llama automáticamente cuando llega un mensaje al grupo
    async def notificacion_pedido(self, event):
        await self.send(text_data=json.dumps(event['data']))