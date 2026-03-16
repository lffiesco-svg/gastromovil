from django import forms
from .models import Restaurante, Categoria, Producto

class RestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields =['nombre', 'direccion', 'telefono', 'activo', 'imagen']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows':2}),
        }