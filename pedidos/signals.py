from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Pedido

@receiver(post_save, sender=Pedido)
def notificar_cambio_pedido(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    # Pedido nuevo → avisar al restaurante
    if created:
        async_to_sync(channel_layer.group_send)(
            f"restaurante_{instance.restaurante.id}",
            {
                "type": "nuevo_pedido",
                "pedido_id": instance.id,
                "cliente": instance.cliente.get_full_name(),
                "total": str(instance.total),
            }
        )

    # Restaurante aceptó → avisar a todos los repartidores disponibles
    elif instance.estado == 'aceptado':
        async_to_sync(channel_layer.group_send)(
            "repartidores_disponibles",  # grupo compartido
            {
                "type": "pedido_disponible",
                "pedido_id": instance.id,
                "restaurante": instance.restaurante.nombre,
                "direccion": str(instance.direccion_entrega),
            }
        )