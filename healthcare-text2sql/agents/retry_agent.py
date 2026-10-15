from src.llm_client import generate
from src.prompt_loader import load_schema
from src.sql_generator import validate_generated_sql


RETRY_SYSTEM_PROMPT = (
    "You are an expert SQLite developer. Return exactly one valid, read-only "
    "SQLite SELECT query and nothing else. Do not include reasoning, "
    "explanations, or Markdown."
)


def retry(question: str, sql: str, error: str) -> str:
    """Generate an improved query using the previous SQL and its failure."""
    prompt = (
        "Use only the schema below. Correct the previous query so that it "
        "answers the question and addresses the reported failure. Do not "
        "repeat the failed query unchanged. Use only real schema columns. "
        "SQL functions are not column names: write COUNT(*) or "
        "COUNT(DISTINCT table.column), never a bare COUNT identifier. "
        "Only use COUNT when the question asks for a number. For cardiologist "
        "requests, filter doctors.specialization = 'Cardiology'.\n\n"
        f"Schema:\n{load_schema()}\n\n"
        f"Question:\n{question}\n\n"
        f"Previous SQL:\n{sql}\n\n"
        f"Error or judge feedback:\n{error}\n\n"
        "Return exactly one query."
    )
    return validate_generated_sql(
        generate(prompt, system_prompt=RETRY_SYSTEM_PROMPT)
    )