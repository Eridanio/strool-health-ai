from fastapi import APIRouter, Request
from fastapi.responses import Response
from xml.sax.saxutils import escape

from app.database import engine
from sqlalchemy import text

router = APIRouter()

# estado simples por usuário
user_state = {}

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()

    incoming_msg = form_data.get("Body")
    user = form_data.get("From")

    # 🔒 proteção (evita crash)
    if not incoming_msg or not user:
        return Response(
            content='<?xml version="1.0" encoding="UTF-8"?><Response></Response>',
            media_type="application/xml"
        )

    incoming_msg = incoming_msg.strip().lower()

    if user not in user_state:
        user_state[user] = {"step": "menu"}

    state = user_state[user]

    # 🔁 comandos globais
    if incoming_msg in ["menu", "ola", "olá", "oi"]:
        state.clear()
        state["step"] = "menu"

    if incoming_msg in ["voltar", "0"]:
        state.clear()
        state["step"] = "menu"

    # MENU
    if state["step"] == "menu":
        reply = """👋 Bem-vindo à Strool Health AI

Como podemos ajudar?

1️⃣ Marcar consulta  
2️⃣ Ver horários  
3️⃣ Localização  
4️⃣ Falar com atendente  

Digite 0 para voltar.
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
        state["step"] = "dia"
        reply = "📅 Qual o dia da consulta?"

    # DIA
    elif state["step"] == "dia":
        state["dia"] = incoming_msg
        state["step"] = "mes"
        reply = "📆 Qual o mês? (ex: 4 para Abril)"

    # MÊS
    elif state["step"] == "mes":
        state["mes"] = incoming_msg
        state["step"] = "hora"
        reply = "⏰ Qual horário prefere?"

    # HORA + SALVAR NO BANCO
    elif state["step"] == "hora":
        state["hora"] = incoming_msg

        try:
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO consultas (user_id, nome, idade, dia, mes, hora)
                    VALUES (:user, :nome, :idade, :dia, :mes, :hora)
                """), {
                    "user": user,
                    "nome": state["nome"],
                    "idade": int(state["idade"]),
                    "dia": int(state["dia"]),
                    "mes": int(state["mes"]),
                    "hora": state["hora"]
                })
                conn.commit()

        except Exception as e:
            print("ERRO AO SALVAR:", e)

        reply = f"""✅ Consulta marcada!

📋 Detalhes:
Nome: {state["nome"]}
Idade: {state["idade"]}
Data: {state["dia"]}/{state["mes"]}
Hora: {state["hora"]}

Entraremos em contacto em breve.
"""

        state.clear()
        state["step"] = "menu"

    # OUTRAS OPÇÕES
    elif incoming_msg == "2":
        reply = "🕒 Funcionamos das 8h às 17h, de segunda a sexta."

    elif incoming_msg == "3":
        reply = "📍 Estamos localizados em Luanda - Talatona."

    elif incoming_msg == "4":
        reply = "👨‍⚕️ Um atendente irá falar consigo."

    else:
        reply = "❗ Opção inválida. Digite 'menu'."

    # 🔐 segurança XML
    safe_reply = escape(reply)

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>{safe_reply}</Message>
</Response>"""

    return Response(content=twiml_response, media_type="application/xml")