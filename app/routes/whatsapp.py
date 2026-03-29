from fastapi import APIRouter, Request
from fastapi.responses import Response
from xml.sax.saxutils import escape

from app.database import SessionLocal
from app.models import Consulta

router = APIRouter()

user_state = {}

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()

    incoming_msg = form_data.get("Body", "").strip().lower()
    user = form_data.get("From", "")

    if user not in user_state:
        user_state[user] = {"step": "menu"}

    state = user_state[user]

    # 🔁 comandos globais
    if incoming_msg in ["menu", "ola", "olá", "oi"]:
        state["step"] = "menu"

    if incoming_msg == "voltar":
        state["step"] = "menu"

    # MENU
    if state["step"] == "menu":
        reply = """👋 Bem-vindo à Strool Health AI

Como podemos ajudar?

1️⃣ Marcar consulta  
2️⃣ Ver horários  
3️⃣ Localização  
4️⃣ Falar com atendente
"""
        if incoming_msg == "1":
            state["step"] = "nome"
            reply = "🧑 Qual é o seu nome?"

    # NOME
    elif state["step"] == "nome":
        state["nome"] = incoming_msg
        state["step"] = "idade"
        reply = "🎂 Qual é a sua idade?"

    # IDADE
    elif state["step"] == "idade":
        state["idade"] = incoming_msg
        state["step"] = "data"
        reply = "📅 Qual dia e mês? (ex: 25/03)"

    # DATA
    elif state["step"] == "data":
        state["data"] = incoming_msg
        state["step"] = "hora"
        reply = "⏰ Qual horário? (ex: 10h)"

    # HORA + SALVAR
    elif state["step"] == "hora":
        state["hora"] = incoming_msg

        db = SessionLocal()

        nova_consulta = Consulta(
            nome=state["nome"],
            idade=state["idade"],
            data=state["data"],
            hora=state["hora"],
            telefone=user
        )

        db.add(nova_consulta)
        db.commit()
        db.close()

        reply = f"""✅ Consulta marcada com sucesso!

📋 Detalhes:
Nome: {state["nome"]}
Idade: {state["idade"]}
Data: {state["data"]}
Hora: {state["hora"]}

Entraremos em contacto em breve.
"""

        state["step"] = "menu"

    else:
        reply = "Digite 'menu' para começar."

    safe_reply = escape(reply)

    twiml_response = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{safe_reply}</Message></Response>'

    return Response(content=twiml_response, media_type="text/xml")