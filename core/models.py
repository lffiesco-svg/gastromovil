from django.db import models

class Restaurante(models.Model):
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    direccion   = models.CharField(max_length=200, blank=True)
    telefono    = models.CharField(max_length=20, blank=True)
    activo      = models.BooleanField(default=True)
    creado_en   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Restaurantes"


class Categoria(models.Model):
    nombre      = models.CharField(max_length=80)
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.CASCADE, related_name='categorias'
    )

    def __str__(self):
        return f"{self.nombre} - {self.restaurante.nombre}"

    class Meta:
        verbose_name_plural = "Categorías"


class Producto(models.Model):
    nombre      = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    imagen      = models.ImageField(upload_to='productos/', blank=True, null=True)
    disponible  = models.BooleanField(default=True)
    creado_en   = models.DateTimeField(auto_now_add=True)
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.CASCADE, related_name='productos'
    )
    categoria   = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos'
    )

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    class Meta:
        verbose_name_plural = "Productos"