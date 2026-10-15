import sqlglot
from sqlglot import exp

if __package__:
    from .llm_client import generate
    from .prompt_loader import load_prompt, load_schema
else:
    from llm_client import generate
    from prompt_loader import load_prompt, load_schema


def generate_sql(question):
 
    prompt = load_prompt().format(
        schema=load_schema(),
        question=question
    )
 
    return validate_generated_sql(generate(prompt))


def validate_generated_sql(sql):
    try:
        statements = sqlglot.parse(sql, read="sqlite")
    except sqlglot.errors.ParseError as error:
        raise RuntimeError(
            "The model response was not valid SQLite SQL. "
            "Please try the question again."
        ) from error

    if len(statements) != 1 or not isinstance(statements[0], exp.Query):
        raise RuntimeError(
            "The model response was not exactly one SQLite query. "
            "Please try the question again."
        )
 
    return sql.strip()