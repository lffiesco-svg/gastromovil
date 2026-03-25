from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from .serializers import MensajeChatSerializer
from .ai.chatbot import responder_chat
from restaurantes.models import Producto


class ChatView(APIView):
    parser_classes = [JSONParser]  # Forzar parser JSON

    def post(self, request):
        serializer = MensajeChatSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        productos = list(Producto.objects.filter(disponible=True).values(
            'nombre',
            'precio',
            'categoria__nombre',
            'categoria__restaurante__nombre',
        ))

        respuesta = responder_chat(
            mensaje_usuario=data['mensaje'],
            productos=productos,
            historial=data.get('historial', []),
            categoria=data.get('categoria'),
            restaurante=data.get('restaurante'),
        )

        return Response({'respuesta': respuesta}, status=status.HTTP_200_OK)