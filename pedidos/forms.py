from django import forms
from .models import Pedido, DetallePedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['restaurante', 'direccion_entrega', 'notas']
        widgets = {
            'restaurante': forms.Select(attrs={'class': 'form-control'}),
            'direccion_entrega': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class CambiarEstadoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }