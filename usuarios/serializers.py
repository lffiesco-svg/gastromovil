from rest_framework import serializers
from .models import Usuario
from .models import Direccion
from pyisemail import is_email 

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, email):
        import re

        # Regex estricta
        patron = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            raise serializers.ValidationError("Ingresa un correo electrónico válido.")

        # Bloquear dominios temporales
        dominios_bloqueados = [
            'mailinator.com', 'yopmail.com', 'tempmail.com',
            'guerrillamail.com', 'trashmail.com', 'fakeinbox.com'
        ]
        dominio = email.split('@')[1].lower()
        if dominio in dominios_bloqueados:
            raise serializers.ValidationError("No se permiten correos temporales.")

        # Verificar que el correo realmente existe
        if not is_email(email):
            raise serializers.ValidationError("El correo electrónico no existe.")

        return email

    def create(self, validated_data):
        validated_data['rol'] = 'cliente'
        user = Usuario.objects.create_user(**validated_data)
        return user

    
class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'