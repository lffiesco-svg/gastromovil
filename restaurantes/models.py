from django.db import models
from usuarios.models import Usuario

# Create your models here.
class Restaurante(models.Model) :
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='restaurantes')
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='restaurantes/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Categoria(models.Model):
    restaurante = models.ForeignKey(Restaurante , on_delete=models.CASCADE, related_name='categoias')
    nombre =models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nombre} - {self.restaurante.nombre}"
    
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre