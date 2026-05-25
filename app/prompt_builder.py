import json


def build_evaluation_prompt(
    student_name: str,
    rubric: dict,
    code: str
) -> str:

    language = rubric.get(
        "language",
        "text"
    )

    rubric_json = json.dumps(
        rubric["criteria"],
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
    Analiza el siguiente código {language}
    y evalúalo utilizando esta rúbrica.

    Debes evaluar TODOS los criterios.

    IMPORTANTE:

    - Devuelve SOLO JSON válido
    - NO uses markdown
    - Cada criterio DEBE incluir:
    - criterion_id
    - criterion_name
    - level
    - score
    - feedback

    El campo "feedback" es obligatorio
    y debe contener una observación breve
    sobre el desempeño del alumno.

    Alumno:
    {student_name}

    Rúbrica:
    {rubric_json}

    Código:
    ```{language}
    {code}

    Formato esperado:

    {{
    "student_name": "{student_name}",
    "criteria_results": [
    {{
    "criterion_id": 1,
    "criterion_name": "Uso de operadores",
    "level": "Bueno",
    "score": 10,
    "feedback": "Utiliza operadores correctamente en la mayoría de los casos."
    }}
    ],
    "total_score": 0,
    "general_feedback": "Resumen general del desempeño."
    }}
    """
    return prompt