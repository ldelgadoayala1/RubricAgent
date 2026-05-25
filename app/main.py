from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from app.evaluator import evaluate_student
from app.schemas import EvaluationResponse
from app.config import (
    UPLOADS_DIR,
    DEFAULT_RUBRIC
)

app = FastAPI(
    title="AI Code Evaluator",
    description="API para evaluación automática de código Python",
    version="1.0.0"
)

UPLOADS_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {
        "message": "AI Code Evaluator API funcionando"
    }


@app.post(
    "/evaluate",
    response_model=EvaluationResponse
)
async def evaluate_code(
    student_name: str = Form(...),
    file: UploadFile = File(...),
    rubric_name: str = Form(DEFAULT_RUBRIC)
):

    allowed_extensions = [".py", ".ipynb"]

    file_extension = Path(file.filename).suffix

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Formato no soportado"
        )

    file_path = UPLOADS_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:

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