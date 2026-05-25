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
    - level: Se extrae directamente de la rúbrica por ejemplo (Destacado, Bueno, Básico, Insuficiente)
    - score: Se asigna segun el level, en el campo points, por ejemplo (Destacado: 15, Bueno: 10, Básico: 5, Insuficiente: 1)
    - feedback: Utiliza los mismos feedback del campo description, segun el level. Por ejemplo (Destacado: "El código cumple con todos los requisitos y demuestra un excelente uso de las estructuras de control.", Bueno: "El código cumple con la mayoría de los requisitos y muestra un buen uso de las estructuras de control.", Básico: "El código cumple con algunos requisitos pero tiene áreas de mejora en el uso de las estructuras de control.", Insuficiente: "El código no cumple con los requisitos y muestra un uso deficiente de las estructuras de control.")
    - general_feedback: resumen general del desempeño


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
    "general_feedback": "Resumen general del desempeño."
    }}
    """
    return prompt