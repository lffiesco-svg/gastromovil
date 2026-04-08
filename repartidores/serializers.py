from rest_framework import serializers
from .models import Repartidor, UbicacionRepartidor

class RepartidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repartidor
        fields = '__all__'

class UbicacionRepartidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbicacionRepartidor
        fields = '__all__'