from django.db import models
from django.conf import settings

class Restaurante(models.Model):
    nombre = models.CharField(max_length=100)
    propietario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurante')  # único
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='categorias')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre