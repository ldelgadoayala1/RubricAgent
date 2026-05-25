def normalize_response(response: dict) -> dict:

    normalized_results = []

    criteria_results = response.get(
        "criteria_results",
        []
    )

    for index, item in enumerate(criteria_results):

        criterion_name = (
            item.get("criterion_name")
            or item.get("name")
            or item.get("criterion")
            or item.get("category")
            or f"Criterio {index + 1}"
        )

        level = (
            item.get("level")
            or item.get("performance")
            or "Básico"
        )

        normalized_item = {

            "criterion_id":
                item.get(
                    "criterion_id",
                    index + 1
                ),

            "criterion_name":
                criterion_name,

            "level":
                level,

            "score":
                item.get(
                    "score",
                    0
                ),

            "feedback":
                item.get(
                    "feedback",
                    ""
                )
        }

        normalized_results.append(
            normalized_item
        )

    normalized_response = {

        "student_name":
            response.get(
                "student_name",
                "Desconocido"
            ),

        "criteria_results":
            normalized_results,

        "total_score":
            response.get(
                "total_score",
                0
            ),

        "general_feedback":
            response.get(
                "general_feedback",
                ""
            )
    }

    return normalized_response