# Grimoire AI — RPG Companion

Asistente conversacional especializado en RPGs de mesa y CRPGs. Recuerda tus personajes, builds y campañas a largo plazo.

## Estado actual
Fase 1 — API base con FastAPI y Ollama (Qwen 2.5 7B)

## Qué puede hacer
- Responder lore profundo (dioses, facciones, historia, cosmología)
- Ayudar con builds y theorycrafting (clases, feats, spells, multiclass)
- Evaluar composición de party
- Dar estrategia de combate (rotaciones, buff order, action economy)
- Comparar sistemas (D&D 5e, Pathfinder 1e, Pathfinder 2e)
- Soportar CRPGs específicos (BG3, WOTR, Kingmaker, Solasta, NWN)

## Stack tecnológico
- Python 3.12
- FastAPI + Uvicorn
- Ollama (Qwen 2.5 7B)

## Requisitos previos
- Ollama instalado y corriendo
- Modelo descargado:

```bash
ollama pull qwen2.5:7b
```

## Cómo correr el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/Raigou/rpg-companion-ai.git
cd rpg-companion-ai
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Correr la API
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 5. Probar
Abre http://127.0.0.1:8000/docs

## Ejemplo

Request:
```json
{
  "texto": "What are the best feats for a Paladin in D&D 5e?"
}
```

Response:
```json
{
  "pregunta": "What are the best feats for a Paladin in D&D 5e?",
  "respuesta": "Great Weapon Master and Sentinel are top picks..."
}
```

## Fases del proyecto
- ✅ Fase 1 — FastAPI + Ollama
- 🔜 Fase 2 — Memoria conversacional (PostgreSQL)
- 🔜 Fase 3 — RAG con pgvector
- 🔜 Fase 4 — Agentes con LangGraph
- 🔜 Fase 5 — GitHub Actions + CI/CD
- 🔜 Fase 6 — Frontend React
- 🔜 Fase 7 — Automatización con n8n