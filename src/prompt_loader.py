from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_schema():

    with open(
        PROJECT_ROOT / "schemas" / "schema_context.txt",
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()


def load_prompt():

    with open(
        PROJECT_ROOT / "prompts" / "text_to_sql_prompt.txt",
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()