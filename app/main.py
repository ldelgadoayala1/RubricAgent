from pathlib import Path
from app.rubric_manager import get_available_rubrics

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException
)

from app.evaluator import evaluate_student
from app.schemas import EvaluationResponse
from app.config import (
    UPLOADS_DIR,
    DEFAULT_RUBRIC
)

app = FastAPI(
    title="RubricAgent",
    description="AI-powered rubric evaluation system",
    version="1.0.0"
)

UPLOADS_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():

    return {
        "message": "RubricAgent API funcionando"
    }


from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://200.27.101.243:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.1:8b"
)


@app.get("/health")
def health():

    try:

        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=10
        )

        if response.status_code != 200:

            return {
                "status": "error",
                "api": "online",
                "ollama": "offline",
                "detail": response.text
            }

        data = response.json()

        models = data.get(
            "models",
            []
        )

        model_names = [
            model.get("name")
            for model in models
        ]

        configured_model_exists = (
            OLLAMA_MODEL in model_names
        )

        return {
            "status": (
                "ok"
                if configured_model_exists
                else "warning"
            ),

            "api": "online",

            "ollama": "online",

            "configured_model": OLLAMA_MODEL,

            "configured_model_exists":
                configured_model_exists,

            "models_available":
                model_names,

            "models_count":
                len(model_names)
        }

    except Exception as e:

        return {
            "status": "error",
            "api": "online",
            "ollama": "offline",
            "detail": str(e)
        }

@app.get("/rubrics")
def list_rubrics():

    return {
        "rubrics": get_available_rubrics()
    }

@app.post(
    "/evaluate",
    response_model=EvaluationResponse
)
async def evaluate_code(
    student_name: str = Form(...),
    file: UploadFile = File(...),
    rubric_name: str = Form(...)
):

    try:

        # Crear path
        file_path = UPLOADS_DIR / file.filename

        # Guardar archivo
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Evaluar
        result = evaluate_student(
            student_name=student_name,
            file_path=str(file_path),
            rubric_name=rubric_name
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
