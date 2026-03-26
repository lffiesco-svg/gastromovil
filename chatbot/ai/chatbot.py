import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .prompts import SYSTEM_PROMPT

load_dotenv()

FRONTEND_BASE_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.5,
    groq_api_key=os.getenv("GROQ_API_KEY")
)


def construir_contexto_productos(productos, categoria=None, restaurante=None):
    """Filtra y formatea los productos para el prompt."""
    filtrados = productos

    if categoria:
        filtrados = [
            p for p in filtrados
            if p['categoria__nombre'] and p['categoria__nombre'].lower() == categoria.lower()
        ]
    if restaurante:
        filtrados = [
            p for p in filtrados
            if p['categoria__restaurante__nombre'] and p['categoria__restaurante__nombre'].lower() == restaurante.lower()
        ]

    if not filtrados:
        return "No hay productos disponibles con ese filtro."

    lineas = []
    for p in filtrados:
        restaurante_id = p['categoria__restaurante__id']
        producto_id = p['id']
        url = f"{FRONTEND_BASE_URL}/restaurante/{restaurante_id}/producto/{producto_id}"
        descripcion = f" | Descripcion: {p['descripcion']}" if p.get('descripcion') else ""
        lineas.append(
            f"- {p['nombre']} | ${p['precio']}"
            f" | Categoria: {p['categoria__nombre'] or 'Sin categoria'}"
            f" | Restaurante: {p['categoria__restaurante__nombre'] or 'Sin restaurante'}"
            f"{descripcion}"
            f" | URL: {url}"
        )

    return "\n".join(lineas)


def responder_chat(mensaje_usuario, productos, historial=None, categoria=None, restaurante=None):
    contexto = construir_contexto_productos(productos, categoria, restaurante)

    prompt_usuario = f"""Productos disponibles:
{contexto}

Pregunta del usuario: {mensaje_usuario}"""

    mensajes = [SystemMessage(content=SYSTEM_PROMPT)]

    if historial:
        for msg in historial[-6:]:
            if msg['role'] == 'user':
                mensajes.append(HumanMessage(content=msg['content']))
            else:
                mensajes.append(AIMessage(content=msg['content']))

    mensajes.append(HumanMessage(content=prompt_usuario))

    try:
        respuesta = llm.invoke(mensajes)
        return respuesta.content
    except Exception as e:
        print(f"[ERROR Groq]: {e}")
        return "Error al procesar tu consulta. Intenta de nuevo mas tarde."
