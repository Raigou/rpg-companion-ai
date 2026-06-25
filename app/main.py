import os
from fastapi import FastAPI
from pydantic import BaseModel
from ollama import Client
from app.memory import get_session_history, save_message

from dotenv import load_dotenv
load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

client = Client(host=OLLAMA_HOST)

app = FastAPI(title="Grimoire AI — RPG Companion")

SYSTEM_PROMPT = """Eres Grimoire, un companion experto en RPGs de mesa y CRPGs.
Tienes conocimiento profundo de:
- D&D 5e, Pathfinder 1e y 2e
- CRPGs: Baldur's Gate 3, Pathfinder WOTR, Kingmaker, Solasta, NWN
- Lore, builds, feats, spells, multiclass, party composition
- Estrategia de combate, action economy, buff order

Responde siempre en el mismo idioma que el usuario.
Sé preciso, detallado y apasionado por los RPGs."""

class Mensaje(BaseModel):
    session_id: str
    texto: str

@app.get("/")
def root():
    return {
        "status": "ok",
        "assistant": "Grimoire AI",
        "environment": APP_ENV
    }

@app.post("/chat")
def chat(mensaje: Mensaje):
    # Recuperar historial de Redis
    historial = get_session_history(mensaje.session_id)

    # Construir mensajes con historial
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(historial)
    messages.append({"role": "user", "content": mensaje.texto})

    # Llamar a Qwen
    respuesta = client.chat(
        model="qwen2.5:7b",
        messages=messages
    )

    respuesta_texto = respuesta.message.content

    # Guardar en Redis y PostgreSQL
    save_message(mensaje.session_id, "user", mensaje.texto)
    save_message(mensaje.session_id, "assistant", respuesta_texto)

    return {
        "session_id": mensaje.session_id,
        "pregunta": mensaje.texto,
        "respuesta": respuesta_texto
    }