import json
import os
import httpx
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from services.tts_service import speak
from graph.langraph_service_integration import graph_compiled
import time

load_dotenv()

PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

processed_messages = set()


def is_valid_whatsapp_message(body):
    """
    Verifica si el evento del webhook tiene una estructura válida de mensaje de WhatsApp.
    """
    return (
            body.get("object")
            and body.get("entry")
            and body["entry"][0].get("changes")
            and body["entry"][0]["changes"][0].get("value")
            and body["entry"][0]["changes"][0]["value"].get("messages")
            and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )


async def process_whatsapp_message(body):
    """
    Procesa un mensaje recibido de WhatsApp y genera una respuesta adecuada.
    """
    print("-------BODY-------")
    print(body)

    # Extraer datos del mensaje
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_id = message["id"]
    timestamp = int(message["timestamp"])

    # Validaciones iniciales
    current_time = int(time.time())
    if current_time - timestamp > 300:  # 5 minutos
        print(f"Mensaje {message_id} es demasiado antiguo, ignorando")
        return
    if message_id in processed_messages:
        print(f"Mensaje {message_id} ya procesado, ignorando")
        return
    processed_messages.add(message_id)

    if message["from"] == PHONE_NUMBER_ID:
        print("Ignorando mensaje enviado por el chatbot")
        return

    # Extraer información del contacto
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
    text_body = message["text"]["body"]

    # Procesar el mensaje con el grafo
    state = {"messages": [HumanMessage(content=text_body)]}
    config = {"configurable": {"thread_id": wa_id}}
    result_state = graph_compiled.invoke(state, config=config)
    message_receive = result_state["messages"][-1].content
    print("---message received---")
    print(message_receive)

    # Determinar el tipo de mensaje
    print("----------type of message-------------")
    type_message = result_state["preferred_response"]
    print(type_message)

    # Preparar el contenido según el tipo de mensaje
    content_to_send = None
    if type_message == "text":
        content_to_send = {"type": "text", "content": message_receive}
    elif type_message == "audio":
        audio_data = await speak(message_receive)
        if audio_data is None:
            print("Error al generar el audio")
            content_to_send = {"type": "text", "content": "Error al generar el audio."}
        else:
            content_to_send = {"type": "audio", "content": audio_data}
    else:
        print("Tipo de mensaje no soportado")
        return

    # Preparar el mensaje para enviar
    data_to_send = await message_prepare_to_send_type(
        wa_id,
        content_to_send["type"],
        content_to_send["content"],
        ""
    )

    if data_to_send is None:
        print("No se pudo preparar el mensaje, abortando envío")
        return

    print("---data to send---")
    print(data_to_send)
    return await send_message(data_to_send)


async def message_prepare_to_send_type(recipient, message_type, content, description):
    """
    Prepara el mensaje en el formato adecuado según el tipo (texto, imagen o audio).
    """
    # Estructura base común para todos los mensajes
    base_message = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"+{recipient}",
        "type": message_type,
    }

    # Manejo según el tipo de mensaje
    if message_type == "text":
        base_message["text"] = {"preview_url": False, "body": content}
    elif message_type == "audio":
        media_result = await process_media_for_whatsapp(content)
        if media_result is None:
            print(f"Error al procesar el media para {message_type}")
            base_message["type"] = "text"
            base_message["text"] = {"preview_url": False, "body": f"Error al procesar el {message_type}."}
        else:
            base_message[message_type] = {"id": media_result["id"]}
    else:
        print("Tipo de mensaje no soportado")
        return None

    return json.dumps(base_message)


async def process_media_for_whatsapp(media):
    """
    Sube el medio (imagen o audio) a la API de WhatsApp y devuelve el ID del medio.
    """
    try:
        media_bytes, mime_type = media
        url = f'https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/media'
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        data = {'messaging_product': 'whatsapp'}
        files = {'file': ('media', media_bytes, mime_type)}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=data, files=files)
        if response.status_code != 200:
            print(f"Error en la API: {response.status_code} - {response.text}")
            return None
        print("Media subida con éxito", response.json())
        return response.json()
    except ValueError as ve:
        print(f"Error de formato en media: {ve}")
        return None
    except httpx.RequestError as re:
        print(f"Error de red: {re}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None


async def send_message(data):
    """
    Envía el mensaje preparado a la API de WhatsApp.
    """
    print("----sending message----")
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print(f"Error al enviar mensaje: {response.status_code} - {response.text}")
        return None
    return response.json()
