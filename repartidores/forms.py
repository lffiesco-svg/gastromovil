from django import forms
from .models import Repartidor, UbicacionRepartidor


class RepartidorForm(forms.ModelForm):
    class Meta:
        model = Repartidor
        fields = ['usuario', 'estado', 'activo']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }


class UbicacionRepartidorForm(forms.ModelForm):
    class Meta:
        model = UbicacionRepartidor
        fields = ['latitud', 'longitud']
        widgets = {
            'latitud': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
        }
        