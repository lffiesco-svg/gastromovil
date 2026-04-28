from django.db import models
from django.conf import settings

class Restaurante(models.Model):
    nombre = models.CharField(max_length=100)
    propietario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurante')  # único
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
from django.core.exceptions import ValidationError
from PIL import Image as PilImage
from usuarios.models import Usuario


# ── Validadores ───────────────────────────────────────────────────────────────

def validar_png(imagen):
    if not imagen.name.lower().endswith('.png'):
        raise ValidationError('Solo se permiten imágenes en formato PNG.')

def validar_dimensiones_restaurante(imagen):
    img = PilImage.open(imagen)
    ancho, alto = img.size
    if ancho != 400 or alto != 250:
        raise ValidationError(
            f'La imagen debe ser exactamente 400×250 px. '
            f'La tuya es {ancho}×{alto} px.'
        )


# ── Modelos ───────────────────────────────────────────────────────────────────

class Restaurante(models.Model):
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='restaurantes')
    nombre      = models.CharField(max_length=200)
    direccion   = models.CharField(max_length=200)
    telefono    = models.CharField(max_length=15)
    activo      = models.BooleanField(default=True)
    imagen      = models.ImageField(
                    upload_to='restaurantes/',
                    blank=True,
                    null=True,
                    validators=[validar_png, validar_dimensiones_restaurante],
                    help_text='PNG de exactamente 400×250 px con fondo transparente.'
                  )

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

class Categoria(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='categoias')
    nombre      = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.restaurante.nombre}"


class Producto(models.Model):
    categoria   = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    nombre      = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    disponible  = models.BooleanField(default=True)
    imagen      = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre