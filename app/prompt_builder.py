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

    experience = rubric.get(
        "experience",
        "No especificada"
    )

    restrictions = rubric.get(
        "restrictions",
        "No hay restricciones adicionales."
    )

    exercises = rubric.get(
        "exercises",
        []
    )

    if isinstance(exercises, list) and exercises:

        formatted_exercises = "\n\n".join(

            f"Ejercicio {item.get('id', '')}:\n"
            f"{item.get('description', '').strip()}"

            for item in exercises
        )

    else:

        formatted_exercises = (
            "No hay ejercicios específicos."
        )

    rubric_json = json.dumps(

        rubric["criteria"],

        ensure_ascii=False,

        indent=2
    )

    prompt = f"""
    Analiza el siguiente código {language}
    y evalúalo utilizando esta rúbrica.

    Contexto del estudiante:
    {experience}

    Restricciones de la evaluación:
    {restrictions}

    Ejercicios específicos:
    {formatted_exercises}

    FILOSOFÍA DE EVALUACIÓN:

    - La evaluación debe centrarse principalmente en si el estudiante logró resolver el problema solicitado.
    - Prioriza programas funcionales aunque no sean perfectos.
    - Evalúa considerando estudiantes de primer año.
    - No exijas estándares profesionales.
    - Valora el esfuerzo, la lógica y la intención correcta.
    - No penalices fuertemente:
        * Código repetitivo
        * Falta de optimización
        * Validaciones incompletas
        * Estilo de código
        * Nombres de variables
        * Ausencia de buenas prácticas avanzadas
        * Soluciones largas o poco elegantes

    IMPORTANTE SOBRE LOS PUNTAJES:

    - Un programa funcional aunque imperfecto puede obtener niveles altos.
    - Si el ejercicio principal está resuelto, el estudiante debería obtener entre 70 y 100 puntos.
    - Si el programa funciona y cumple la mayoría de los requisitos, prioriza niveles "Bueno" o "Destacado".
    - Usa "Insuficiente" SOLO cuando el criterio prácticamente no exista o el programa no funcione.
    - Si hay duda entre dos niveles, elige el nivel superior.

    Debes evaluar TODOS los criterios.

    IMPORTANTE:

    - Devuelve SOLO JSON válido
    - NO uses markdown
    - NO agregues texto fuera del JSON
    - Identifica de cuál ejercicio se trata
    - Evalúa cada criterio considerando el contexto del estudiante
    - Evalúa con indulgencia académica apropiada para primer año

    Cada criterio DEBE incluir:

    - criterion_id
    - criterion_name
    - level
    - score
    - feedback

    El campo "level" debe existir exactamente
    en la rúbrica.

    El campo "score" debe corresponder
    al puntaje asociado al nivel.

    El campo "feedback" debe utilizar la
    descripción del nivel seleccionado.

    El campo "general_feedback" debe:

    - resumir fortalezas
    - mencionar mejoras posibles
    - destacar si el ejercicio funciona
    - valorar el esfuerzo del estudiante

    Alumno:
    {student_name}

    Rúbrica:
    {rubric_json}

    Código:
    ```{language}
    {code}
    ```

    Formato esperado:

    {{
      "student_name": "{student_name}",
      "criteria_results": [
        {{
          "criterion_id": 1,
          "criterion_name": "Uso de operadores",
          "level": "Bueno",
          "score": 10,
          "feedback": "Aplica correctamente los operadores en la mayoría de los casos."
        }}
      ],
      "general_feedback": "Resumen general del desempeño."
    }}
    """

    return prompt