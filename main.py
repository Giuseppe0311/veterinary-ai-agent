import os

from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from utils.security import signature_required
from utils.whatsapp_utils import is_valid_whatsapp_message, process_whatsapp_message
from api import companies_api, companies_detail_api, companies_services_api, company_documents_api, auth_api
from middleware.auth import auth_middleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(companies_api.router)
app.include_router(companies_detail_api.router)
app.include_router(companies_services_api.router)
app.include_router(company_documents_api.router)
app.include_router(auth_api.router)

app.middleware("http")(auth_middleware)

load_dotenv()

verify_token_word = os.getenv("WHATSAPP_VERIFY_TOKEN")


async def handle_message(request):
    body = await request.json()
    if (
            body.get("entry", [{}])[0]
                    .get("changes", [{}])[0]
                    .get("value", {})
                    .get("statuses")
    ):
        return Response(status_code=200)

    try:
        if is_valid_whatsapp_message(body):
            await process_whatsapp_message(body)
        else:
            #  raise HTTPException(status_code=404, detail="Not a WhatsApp API event")
            print("Not a WhatsApp API event")
            return Response(status_code=200)  # Ignorar eventos que no sean mensajes de WhatsApp

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def verify(request):
    query_params = request.query_params
    hub_mode = query_params.get('hub.mode')
    hub_challenge = query_params.get('hub.challenge')
    hub_verify_token = query_params.get('hub.verify_token')
    if hub_mode and hub_verify_token:
        if hub_mode == "subscribe" and hub_verify_token == verify_token_word:
            return Response(content=hub_challenge, status_code=200, media_type="text/plain")
        else:
            raise HTTPException(status_code=403, detail="Invalid verification token")
    raise HTTPException(status_code=400, detail="Bad Request: Missing parameters")


@app.get("/webhook")
async def webhook_meta_whatsapp(request: Request):
    return verify(request)


@app.post("/webhook")
@signature_required
async def webhook_meta_whatsapp(request: Request):
    return await handle_message(request)
