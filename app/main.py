from fastapi import FastAPI
from app.routes.whatsapp import router as whatsapp_router
from app.database import create_tables

app = FastAPI(title="Strool Health AI")

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(whatsapp_router)