import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from .prompts import SYSTEM_PROMPT

load_dotenv()

# modelo Llama 3
llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.5,
    groq_api_key=os.getenv("GROQ_API_KEY")
)


def responder_chat(mensaje_usuario, productos):

    contexto_productos = "\n".join(
        [f"{p['nombre']} - ${p['precio']} - categoria {p['categoria']} - restaurante {p['restaurante']}"
         for p in productos]
    )

    prompt = f"""
Estos son los productos disponibles:

{contexto_productos}

Pregunta del usuario:
{mensaje_usuario}
"""

    respuesta = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])

    return respuesta.content

