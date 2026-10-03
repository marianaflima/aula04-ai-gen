import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODELO = os.getenv("GROQ_MODELO")

assert GROQ_API_KEY, \
    "GROQ_API_KEY ausente. Confira .env"

print(f"Modelo GROQ: {GROQ_MODELO} (chave carregada: OK)")