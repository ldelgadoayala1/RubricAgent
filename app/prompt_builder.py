import json


def build_evaluation_prompt(
    student_name: str,
    rubric: dict,
    code: str
) -> str:

    rubric_json = json.dumps(
        rubric,
        indent=2,
        ensure_ascii=False
    )

    prompt = f"""
    Eres un profesor universitario experto en programación Python.
    Debes evaluar el código del alumno utilizando EXCLUSIVAMENTE la siguiente rúbrica.

    RÚBRICA:
    {rubric_json}

    NOMBRE DEL ALUMNO:
    {student_name}

    CÓDIGO DEL ALUMNO:
    ```python
    {code}

    INSTRUCCIONES IMPORTANTES:

    Evalúa TODOS los criterios.
    Para cada criterio selecciona SOLO uno de estos niveles:
    Destacado
    Bueno
    Básico
    Insuficiente
    Justifica brevemente cada evaluación.
    Calcula correctamente el puntaje total.
    NO inventes criterios adicionales.
    RESPONDE SOLO JSON VÁLIDO.

    FORMATO DE RESPUESTA:

    {{
    "student_name": "{student_name}",
    "criteria_results": [
    {{
    "criterion_id": 1,
    "criterion_name": "",
    "level": "",
    "score": 0,
    "feedback": ""
    }}
    ],
    "total_score": 0,
    "general_feedback": ""
    }}
    """
    return prompt