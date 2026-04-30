import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import UbicacionRepartidor


class UbicacionConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.repartidor_id = self.scope['url_route']['kwargs']['repartidor_id']
        self.group_name = f'ubicacion_{self.repartidor_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitud = data.get('latitud')
        longitud = data.get('longitud')

        await self.guardar_ubicacion(latitud, longitud)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'ubicacion_actualizada',
                'latitud': latitud,
                'longitud': longitud,
            }
        )

    async def ubicacion_actualizada(self, event):
        await self.send(text_data=json.dumps({
            'latitud': event['latitud'],
            'longitud': event['longitud'],
        }))

    @database_sync_to_async
    def guardar_ubicacion(self, latitud, longitud):
        from usuarios.models import Usuario
        try:
            usuario = Usuario.objects.get(id=self.repartidor_id)
            UbicacionRepartidor.objects.update_or_create(
                repartidor=usuario,
                defaults={'latitud': latitud, 'longitud': longitud}
            )
        except Usuario.DoesNotExist:
            pass


class RepartidorConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.repartidor_id = self.scope['url_route']['kwargs']['repartidor_id']
        self.group_name = f'repartidor_{self.repartidor_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def notificacion_pedido(self, event):
        await self.send(text_data=json.dumps(event['data']))
