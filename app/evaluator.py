from pathlib import Path


from app.notebook_parser import extract_code_from_notebook
from app.prompt_builder import build_evaluation_prompt
from app.llm_client import evaluate_with_llm
from app.rubric import load_rubric
from app.response_parser import normalize_response

def read_code_file(file_path: str) -> str:

    path = Path(file_path)

    if path.suffix == ".py":

        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    elif path.suffix == ".ipynb":

        return extract_code_from_notebook(file_path)

    else:
        raise ValueError(
            "Formato de archivo no soportado"
        )


def evaluate_student(
    student_name: str,
    file_path: str,
    rubric_name: str
) -> dict:

    rubric = load_rubric(rubric_name)

    code = read_code_file(file_path)

    prompt = build_evaluation_prompt(
        student_name=student_name,
        rubric=rubric,
        code=code
    )

    result = evaluate_with_llm(
        prompt=prompt,
        student_name=student_name
    )

    normalized_result = normalize_response(
        result
    )

    return normalized_result
    