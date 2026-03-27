from fastapi import FastAPI
from app.routes.whatsapp import router as whatsapp_router

app = FastAPI(title="Strool Health AI")

app.include_router(whatsapp_router)