from fastapi import APIRouter, Form
from fastapi.responses import Response
from app.services.ai_service import get_ai_response

router = APIRouter()

@router.post("/webhook")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    
    resposta = get_ai_response(From, Body)

    twiml = f"""
    <Response>
        <Message>{resposta}</Message>
    </Response>
    """

    return Response(content=twiml, media_type="application/xml")