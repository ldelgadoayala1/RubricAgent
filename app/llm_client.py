import json
import requests
from pathlib import Path


# =====================================================
# Cargar configuración
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent

CONFIG_PATH = PROJECT_ROOT / "gestion-uso-ia-config.json"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

BASE_URL = CONFIG["base_url"].rstrip("/")
API_KEY = CONFIG["api_key"]

CHAT_URL = BASE_URL + CONFIG["endpoints"]["chat_completions"]

# Modelo por defecto
MODEL = "gemma4:e2b"


# =====================================================
# Cliente LLM
# =====================================================

def evaluate_with_llm(
    prompt: str,
    student_name: str
) -> dict:

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {

        "model": MODEL,

        "messages": [

            {
                "role": "system",
                "content": """
Eres un evaluador automático de código.

Tu única tarea es responder JSON válido.

NO expliques.
NO converses.
NO des ejemplos.
NO escribas markdown.

La respuesta DEBE ser JSON válido.
"""
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        "temperature": 0

    }

    response = requests.post(
        CHAT_URL,
        headers=headers,
        json=payload,
        timeout=300
    )

    if response.status_code != 200:

        raise Exception(
            f"""
Error llamando al LLM.

Status:
{response.status_code}

Respuesta:
{response.text}
"""
        )

    raw_response = response.json()

    content = raw_response["choices"][0]["message"]["content"]

    print("\n========== RAW RESPONSE ==========")
    print(content)
    print("==================================\n")

    try:
        return json.loads(content)

    except Exception as e:

        raise Exception(
            f"""
Error parseando JSON.

Error:
{e}

Contenido:
{content}
"""
        )