# 🏥 Strool Health AI

A conversational healthcare assistant built with **FastAPI** and **Twilio WhatsApp** to automate patient interactions for healthcare clinics.

---

## 📌 Overview

Strool Health AI is a backend application designed to streamline communication between healthcare providers and patients through WhatsApp.

The system automates appointment scheduling, provides clinic information, and manages structured conversations using a modular backend architecture built with FastAPI.

---

## ✨ Features

- 💬 WhatsApp chatbot integration
- 📅 Automated appointment scheduling
- 👤 Patient information collection
- 🔄 Conversation state management
- ⚡ FastAPI REST API
- 🗄️ Database integration with SQLAlchemy
- ☁️ Cloud deployment configuration (Render)

---

## 🏗️ Architecture

```text
Patient
   │
WhatsApp
   │
Twilio API
   │
FastAPI Backend
   │
Conversation Engine
   │
PostgreSQL Database
```

---

## 📂 Project Structure

```text
strool-health-ai/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   │
│   ├── routes/
│   │   └── whatsapp.py
│   │
│   └── services/
│       └── ai_service.py
│
├── requirements.txt
├── render.yaml
├── start.sh
└── README.md
```

---

## 🛠️ Technologies

### Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy

### Messaging

- Twilio WhatsApp API

### Database

- PostgreSQL

### Deployment

- Render

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/Eridanio/strool-health-ai.git
```

Go to the project directory:

```bash
cd strool-health-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=your_database_url
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
```

Run the application:

```bash
uvicorn app.main:app --reload
```

---

## 🔄 Conversation Flow

```text
User
   │
   ▼
WhatsApp Message
   │
   ▼
Twilio Webhook
   │
   ▼
FastAPI Endpoint
   │
   ▼
Conversation Engine
   │
   ▼
Database
   │
   ▼
Response sent back to WhatsApp
```

---

## 🌍 Deployment

The project includes deployment configuration for **Render**.

Current project status:

- ✅ Backend architecture completed
- ✅ WhatsApp webhook integration
- ✅ Database layer implemented
- 🟡 Cloud deployment in progress

---

## 🔮 Roadmap

- Integrate Large Language Models (LLMs)
- User authentication
- Administrative dashboard
- Persistent conversation history
- Docker support
- Automated testing
- Monitoring and logging

---

## 👨‍💻 Author

**Adilson Eridanio**

Computer Engineering and Information Systems Student

Founder of **BizPulse Strool AI**

- GitHub: https://github.com/Eridanio
- LinkedIn: https://www.linkedin.com/in/adilson-eridanio-900a9337a

---

⭐ *Building intelligent software solutions with Artificial Intelligence and modern software engineering.*