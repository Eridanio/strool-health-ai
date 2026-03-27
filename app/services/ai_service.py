import os
from dotenv import load_dotenv
##from openai import OpenAI

##load_dotenv()  # Carrega variáveis do .env

##client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

user_states = {}
user_data = {}
consultas = []

def get_ai_response(user, message: str) -> str:
    message = message.lower().strip()

    state = user_states.get(user, "menu")

    # MENU
    if message in ["ola", "olá", "menu", "oi"]:
        user_states[user] = "menu"
        user_data[user] = {}
        return """👋 Bem-vindo à *Strool Health AI*

Como podemos ajudar?

1️⃣ Marcar consulta  
2️⃣ Ver horários  
3️⃣ Localização  
4️⃣ Falar com atendente  
"""

    # OPÇÃO 1 - MARCAR CONSULTA
    if message == "1":
        user_states[user] = "nome"
        user_data[user] = {}
        return "🧑 Qual é o seu nome?"

    # NOME
    if state == "nome":
        user_data[user]["nome"] = message.title()
        user_states[user] = "data"
        return "📅 Para que dia deseja marcar?"

    # DATA
    if state == "data":
        user_data[user]["data"] = message
        user_states[user] = "hora"
        return "⏰ Qual horário prefere?"

    # HORA
    if state == "hora":
        user_data[user]["hora"] = message

        # 💾 SALVAR CONSULTA
        consulta = {
            "user": user,
            "nome": user_data[user]["nome"],
            "data": user_data[user]["data"],
            "hora": user_data[user]["hora"]
        }

        consultas.append(consulta)

        # Reset estado
        user_states[user] = "menu"

        return f"""✅ Consulta marcada com sucesso!

📋 Detalhes:
Nome: {consulta['nome']}
Data: {consulta['data']}
Hora: {consulta['hora']}

Entraremos em contacto em breve."""

    # OPÇÃO 2
    if message == "2":
        return "🕒 Funcionamos das 8h às 17h, de segunda a sexta."

    # OPÇÃO 3
    if message == "3":
        return "📍 Estamos localizados em Luanda no municipio do Talatona."

    # OPÇÃO 4
    if message == "4":
        return "👨‍⚕️ Um atendente irá falar consigo em breve."

    return "❗ Opção inválida. Digite *menu* para voltar."
