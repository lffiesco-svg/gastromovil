import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .prompts import SYSTEM_PROMPT

load_dotenv()

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.5,
    groq_api_key=os.getenv("GROQ_API_KEY")
)


def construir_contexto_productos(productos, categoria=None, restaurante=None):
    """Filtra y formatea los productos para el prompt."""
    filtrados = productos

    if categoria:
        filtrados = [p for p in filtrados if p['categoria__nombre'] and p['categoria__nombre'].lower() == categoria.lower()]
    if restaurante:
        filtrados = [p for p in filtrados if p['restaurante__nombre'] and p['restaurante__nombre'].lower() == restaurante.lower()]

    if not filtrados:
        return "No hay productos disponibles con ese filtro."

    return "\n".join(
        [f"- {p['nombre']} | ${p['precio']} | Categoría: {p['categoria__nombre'] or 'Sin categoría'} | Restaurante: {p['restaurante__nombre']}"
         for p in filtrados]
    )


def responder_chat(mensaje_usuario, productos, historial=None, categoria=None, restaurante=None):
    """
    Responde al usuario con contexto de productos e historial.

    historial: lista de dicts [{role: 'user'|'assistant', content: '...'}]
    """
    contexto = construir_contexto_productos(productos, categoria, restaurante)

    prompt_usuario = f"""Productos disponibles:
{contexto}

Pregunta: {mensaje_usuario}"""

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
        return "Error al procesar tu consulta. Intenta de nuevo más tarde."
    