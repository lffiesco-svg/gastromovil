from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser) :
    ROLES = [
        ('cliente' , 'Cliente'),
        ('repartidor' ,'Repartidor'),
        ('restautante' , 'Restaurante'),
    ]

    telefono = models.CharField(max_length= 15, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')

    def __str__(self):
        return f"{self.username} - {self.rol}"
    
class Direccion(models.Model) :
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='direcciones')
    calle = models.CharField(max_length=200)
    barrio = models.CharField(max_length=100)
    referencia = models.CharField(max_length=200, blank=True)
    es_principal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.calle}, {self.barrio}"