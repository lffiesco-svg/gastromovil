from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from restaurantes.models import Restaurante
from django.db.models.signals import post_save
from django.dispatch import receiver
from restaurantes.models import Restaurante

# Create your models here.
class Usuario(AbstractUser):
    ROLES = [
        ('cliente', 'Cliente'),
        ('repartidor', 'Repartidor'),
        ('restaurante', 'Restaurante'),
    ]

    telefono = models.CharField(max_length=15, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} - {self.rol}"

    def save(self, *args, **kwargs):  # ← debe estar DENTRO de la clase
        if self.rol == 'restaurante':
            self.is_staff = True
        elif not self.is_superuser:
            self.is_staff = False
        super().save(*args, **kwargs)

class Direccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='direcciones')
    calle = models.CharField(max_length=200)
    barrio = models.CharField(max_length=100)
    referencia = models.CharField(max_length=200, blank=True)
    es_principal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.calle}, {self.barrio}"
    
class Calificacion(models.Model):
    pedido = models.OneToOneField('pedidos.Pedido', on_delete=models.CASCADE, related_name='calificacion') 
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(choices=[(i, i)for i in range(1,6)])
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Calificacion {self.puntuacion}/5 - Pedido #{self.pedido.id}" 
    
class CodigoRecuperacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6)
    creado = models.DateTimeField(auto_now_add=True)
    expiracion = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expiracion

    def save(self, *args, **kwargs):
        if not self.expiracion:
            self.expiracion = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

def save(self, *args, **kwargs):
    if self.rol == 'restautante':
        self.is_staff = True
    elif not self.is_superuser:
        self.is_staff = False
    super().save(*args, **kwargs)


receiver(post_save, sender=Usuario)
def crear_restaurante_para_usuario(sender, instance, created, **kwargs):
    if created and instance.rol == 'restaurante':
        Restaurante.objects.create(
            nombre=f"Restaurante de {instance.first_name}",
            propietario=instance,
            direccion="Dirección pendiente",
            telefono=instance.telefono or "0000000000",
            activo=True
        )