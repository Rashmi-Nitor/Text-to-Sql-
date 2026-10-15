from src.sql_generator import generate_sql as _generate_sql


def generate_sql(question: str) -> str:
    """Generate one read-only SQLite query for a healthcare question."""
    if not question.strip():
        raise ValueError("The question cannot be empty.")

    return _generate_sql(question)