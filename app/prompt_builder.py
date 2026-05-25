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

        Devuelve SOLO JSON válido.

        La respuesta debe comenzar con {{
        y terminar con }}

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
        "criteria_results": [],
        "total_score": 0,
        "general_feedback": ""
        }}
        """
    return prompt