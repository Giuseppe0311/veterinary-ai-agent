import os
from functools import wraps
from fastapi import Request, HTTPException
import logging
import hashlib
import hmac
from dotenv import load_dotenv

load_dotenv()

APP_SECRET = os.getenv("APP_SECRET")


def validate_signature(payload: str, signature: str) -> bool:
    """
    Valida la firma HMAC-SHA256 del payload contra la firma esperada.

    :param payload: Cuerpo de la solicitud como string.
    :param signature: Firma recibida en el encabezado X-Hub-Signature-256.
    :return: True si la firma es válida, False si no.
    """
    expected_signature = hmac.new(
        key=APP_SECRET.encode("utf-8"),
        msg=payload.encode("utf-8"),
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)


def signature_required(f):
    """
    Decorador para asegurar que las solicitudes entrantes al webhook estén firmadas correctamente.
    """

    @wraps(f)
    async def decorated_function(request: Request, *args, **kwargs):
        signature = request.headers.get("X-Hub-Signature-256", "")
        if not signature.startswith("sha256="):
            logging.info("Formato de firma inválido")
            raise HTTPException(status_code=403, detail="Invalid signature format")

        signature = signature[7:]

        body = await request.body()
        payload = body.decode("utf-8")

        if not validate_signature(payload, signature):
            logging.info("Verificación de firma fallida!")
            raise HTTPException(status_code=403, detail="Invalid signature")

        return await f(request, *args, **kwargs)

    return decorated_function
