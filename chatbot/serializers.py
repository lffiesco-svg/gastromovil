from rest_framework import serializers


class MensajeChatSerializer(serializers.Serializer):
    mensaje = serializers.CharField(max_length=500)
    categoria = serializers.CharField(required=False, allow_blank=True)
    restaurante = serializers.CharField(required=False, allow_blank=True)
    historial = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list
    )