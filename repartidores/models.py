from django.db import models
from usuarios.models import Usuario


# Create your models here.
class Repartidor(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('inactivo', 'Inactivo'),
    ]

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='repartidor')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='inactivo')
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.estado}"
    
class UbicacionRepartidor (models.Model):
    repartidor = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='ubicacion')
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    actualizado = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Ubicacion de {self.repartidor.username}" 