import os
from fastapi import FastAPI
from pydantic import BaseModel
from ollama import Client

APP_ENV = os.getenv("APP_ENV", "development")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

client = Client(host=OLLAMA_HOST)

app = FastAPI(title="Grimoire AI — RPG Companion")

# System prompt — define el comportamiento del asistente
SYSTEM_PROMPT = """Eres Grimoire, un companion experto en RPGs de mesa y CRPGs.
Tienes conocimiento profundo de:
- D&D 5e, Pathfinder 1e y 2e
- CRPGs: Baldur's Gate 3, Pathfinder WOTR, Kingmaker, Solasta, NWN
- Lore, builds, feats, spells, multiclass, party composition
- Estrategia de combate, action economy, buff order

Responde siempre en el mismo idioma que el usuario.
Sé preciso, detallado y apasionado por los RPGs."""

class Mensaje(BaseModel):
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
    respuesta = client.chat(
        model="qwen2.5:7b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": mensaje.texto}
        ]
    )
    return {
        "pregunta": mensaje.texto,
        "respuesta": respuesta.message.content
    }
