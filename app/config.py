from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RUBRICS_DIR = BASE_DIR / "rubrics"
UPLOADS_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"

DEFAULT_RUBRIC = "python_basico.json"

OPENAI_MODEL = "gpt-4.1-mini"

MAX_FILE_SIZE_MB = 10