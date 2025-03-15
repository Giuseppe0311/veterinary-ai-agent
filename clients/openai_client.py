import websocket
from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def websocket_instante():
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
    headers = [
        "Authorization: Bearer " + OPENAI_API_KEY,
        "OpenAI-Beta: realtime=v1"
    ]
    return  websocket.WebSocketApp(
        url=url,
        header=headers
    )

