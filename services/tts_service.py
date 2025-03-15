from google.cloud import texttospeech
from dotenv import load_dotenv
from google.cloud.texttospeech_v1 import SynthesisInput
import logging
import asyncio

load_dotenv()

client = texttospeech.TextToSpeechClient(credentials="./keys/titanium-haiku-451321-e2-b26a209d77da.json")

voice = texttospeech.VoiceSelectionParams(
    name="es-US-Chirp3-HD-Charon",
    language_code="es-US"
)


async def speak(message: str):
    print("-----starting speak----")
    try:
        if not message:
            raise ValueError("The message provided is empty.")

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.OGG_OPUS,
        )

        synthesis_input = SynthesisInput(text=message)

        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
            timeout=60
        )

        if not response.audio_content:
            raise RuntimeError("No audio content was generated from the synthesis.")

        return response.audio_content, "audio/ogg"

    except Exception as e:
        logging.error(f"An error occurred during speech synthesis: {e}")
        raise
