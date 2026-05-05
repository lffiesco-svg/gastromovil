import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from .serializers import MensajeChatSerializer
from .ai.chatbot import responder_chat
from restaurantes.models import Producto


class ChatView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = MensajeChatSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        mensaje = data['mensaje']

        productos = list(Producto.objects.filter(disponible=True).values(
            'id',
            'nombre',
            'descripcion',
            'precio',
            'imagen',
            'categoria__id',
            'categoria__nombre',
            'categoria__restaurante__id',
            'categoria__restaurante__nombre',
        ))

        # Si es modo sorpresa, elegir producto aleatorio y pedir solo la razón
        palabras_sorpresa = ['sorpréndeme', 'sorprendeme', 'recomiéndame', 'recomiendame', 'sorpresa']
        es_sorpresa = any(p in mensaje.lower() for p in palabras_sorpresa)

        if es_sorpresa and productos:
            producto = random.choice(productos)
            restaurante_id = producto['categoria__restaurante__id']
            categoria_id = producto['categoria__id']
            imagen = producto.get('imagen') or ''
            imagen_url = f"http://localhost:8000/media/{imagen}" if imagen else ''
            url = f"http://localhost:8000/restaurantes/restaurante/{restaurante_id}/#cat-{categoria_id}"

            # Pedirle al LLM solo la razón
            from .ai.chatbot import responder_razon
            razon = responder_razon(producto)

            import json
            respuesta = json.dumps({
                "modo": "sorpresa",
                "producto_id": producto['id'],
                "nombre": producto['nombre'],
                "precio": str(producto['precio']),
                "restaurante": producto['categoria__restaurante__nombre'] or '',
                "descripcion": producto['descripcion'] or '',
                "url": url,
                "imagen": imagen_url,
                "razon": razon,
            }, ensure_ascii=False)

            return Response({'respuesta': respuesta}, status=status.HTTP_200_OK)

        # Flujo normal del chatbot
        respuesta = responder_chat(
            mensaje_usuario=mensaje,
            productos=productos,
            historial=data.get('historial', []),
            categoria=data.get('categoria'),
            restaurante=data.get('restaurante'),
        )

        return Response({'respuesta': respuesta}, status=status.HTTP_200_OK)
