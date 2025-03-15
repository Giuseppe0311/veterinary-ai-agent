from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from config.llm_models import llm_openai

@tool
def response_general(query: str) -> str:
    """RESPONDE A PREGUNTAS VETERINARIAS Y SALUDOS.
    Contexto de uso:
    - Responderás sobre medicina veterinaria, cuidado de mascotas y saludos
    - Ignorarás preguntas sobre humanos, temas no médicos o fuera de contexto
    - Para conversaciones no relacionadas, usarás unhandled_messages
    - Mantendrás respuestas profesionales pero comprensivas

    Ejemplos válidos:
    '¿Qué vacunas necesita un cachorro?'
    'Buenos días, ¿cómo estás?'
    '¿Cómo tratar una herida en la pata de un gato?'

    Ejemplos inválidos:
    'Cómo preparar una pizza' -> [usar unhandled_messages]
    'Dime un chiste' -> [usar unhandled_messages]
    'Historia de la medicina' -> [usar unhandled_messages]"""

    system_message = """Eres un asistente veterinario especializado. 
    Reglas estrictas:
    1. Responder a preguntas sobre animales domésticos y veterinaria.
    2. Responder a saludos de manera apropiada y luego preguntar si tienen alguna pregunta sobre veterinaria.
    3. Para cualquier otro tema, decir que no puedes ayudar.
    4. Mantener respuestas técnicas pero accesibles.
    5. Si la pregunta es ambigua, pedir clarificación.

    Ejemplos:
    - Usuario: 'Hola'
      Asistente: '¡Hola! ¿En qué puedo ayudarte con respecto a tus mascotas?'
    - Usuario: 'Buenos días, ¿cómo estás?'
      Asistente: '¡Buenos días! Estoy bien, gracias. ¿En qué puedo ayudarte con tus mascotas hoy?'
    - Usuario: '¿Qué vacunas necesita un cachorro?'
      Asistente: 'Un cachorro necesita varias vacunas importantes, como la de parvovirus, moquillo, hepatitis, leptospirosis y rabia. Es recomendable consultar con un veterinario para un calendario de vacunación específico.'
    - Usuario: 'Cómo preparar una pizza'
      Asistente: 'No estoy permitido para responder a eso. ¿Puedo ayudarte con algo más?'

    Contexto previo: {history}
    """
    response = llm_openai.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=query)
    ])

    return response.content

@tool
def unhandled_messages(query: str) -> str:
    """RESPONDE A MENSAJES NO MANEJADOS."""
    return "No estoy permitido para responder a eso. ¿Puedo ayudarte con algo más?"

JUST_CALL_TOOLS = [response_general]