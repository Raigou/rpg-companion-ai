import os
import redis
import psycopg2
from datetime import datetime


from dotenv import load_dotenv
load_dotenv()

# Conexión Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)

# Conexión PostgreSQL
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_session_history(session_id: str) -> list:
    # Obtener historial de Redis
    messages = redis_client.lrange(f"session:{session_id}", 0, -1)
    history = []
    for msg in messages:
        role, content = msg.split("|", 1)
        history.append({"role": role, "content": content})
    return history

def save_to_redis(session_id: str, role: str, message: str):
    # Guardar mensaje en Redis
    redis_client.rpush(f"session:{session_id}", f"{role}|{message}")
    # Expirar sesión después de 24 horas
    redis_client.expire(f"session:{session_id}", 86400)

def save_to_postgres(session_id: str, role: str, message: str):
    # Guardar mensaje en PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversations (session_id, role, message)
        VALUES (%s, %s, %s)
    """, (session_id, role, message))
    conn.commit()
    cursor.close()
    conn.close()

def save_message(session_id: str, role: str, message: str):
    save_to_redis(session_id, role, message)
    save_to_postgres(session_id, role, message)