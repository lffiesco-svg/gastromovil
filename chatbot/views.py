from django.shortcuts import render
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import MensajeChatSerializer
from .ai.chatbot import responder_chat
from core.models import Producto  # Ajusta según tu modelo real


class ChatView(APIView):

    def post(self, request):
        serializer = MensajeChatSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Obtener productos de la BD (ajusta el queryset a tu modelo)
        productos = list(Producto.objects.values('nombre', 'precio', 'categoria', 'restaurante'))

        respuesta = responder_chat(
            mensaje_usuario=data['mensaje'],
            productos=productos,
            historial=data.get('historial', []),
            categoria=data.get('categoria'),
            restaurante=data.get('restaurante'),
        )

        return Response({'respuesta': respuesta}, status=status.HTTP_200_OK)