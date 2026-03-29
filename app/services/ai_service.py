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

    # VOLTAR
    if message in ["voltar", "0"]:
        user_states[user] = "menu"
        user_data[user] = {}
        return "🔙 Voltou ao menu.\nDigite *menu* para ver opções."

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

Digite *0* para voltar a qualquer momento.
"""

    # INICIAR CONSULTA
    if message == "1":
        user_states[user] = "nome"
        user_data[user] = {}
        return "🧑 Qual é o seu nome?"

    # NOME
    if state == "nome":
        user_data[user]["nome"] = message.title()
        user_states[user] = "idade"
        return "🎂 Qual é a sua idade?"

    # IDADE
    if state == "idade":
        user_data[user]["idade"] = message
        user_states[user] = "dia"
        return "📅 Qual o dia da consulta?"

    # DIA
    if state == "dia":
        user_data[user]["dia"] = message
        user_states[user] = "mes"
        return "📆 Qual o mês? (ex: 4 para Abril)"

    # MÊS
    if state == "mes":
        user_data[user]["mes"] = message
        user_states[user] = "hora"
        return "⏰ Qual horário prefere?"

    # HORA
    if state == "hora":
        user_data[user]["hora"] = message

        consulta = {
            "user": user,
            "nome": user_data[user]["nome"],
            "idade": user_data[user]["idade"],
            "dia": user_data[user]["dia"],
            "mes": user_data[user]["mes"],
            "hora": user_data[user]["hora"]
        }

        consultas.append(consulta)

        user_states[user] = "menu"

        return f"""✅ Consulta marcada!

📋 Detalhes:
Nome: {consulta['nome']}
Idade: {consulta['idade']}
Data: {consulta['dia']}/{consulta['mes']}
Hora: {consulta['hora']}
"""

    # OUTRAS OPÇÕES
    if message == "2":
        return "🕒 Funcionamos das 8h às 17h, de segunda a sexta."

    if message == "3":
        return "📍 Estamos localizados em Luanda - Talatona."

    if message == "4":
        return "👨‍⚕️ Um atendente irá falar consigo."

    return "❗ Opção inválida. Digite *menu*."