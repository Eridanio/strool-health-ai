from fastapi import APIRouter, Request
from fastapi.responses import Response
from app.services.ai_service import get_ai_response
from xml.sax.saxutils import escape

router = APIRouter()

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    
    incoming_msg = form_data.get("Body", "").strip()
    user = form_data.get("From", "")

    # 🔥 ATIVA O BOT REAL
    reply = get_ai_response(user, incoming_msg)

    # 🔥 Evita erro com caracteres especiais (muito importante)
    safe_reply = escape(reply)

    # 🔥 TwiML correto para o Twilio
    twiml_response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{safe_reply}</Message>
</Response>'''

    return Response(content=twiml_response, media_type="application/xml")