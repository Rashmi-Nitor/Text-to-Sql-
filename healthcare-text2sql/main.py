import sqlite3
from typing import Any, TypedDict

from agents.judge_agent import judge
from agents.retry_agent import retry
from agents.sql_agent import generate_sql
from src.evaluator import execute_query


MAX_ATTEMPTS = 3


class AgentOutcome(TypedDict):
    sql: str
    result: list[tuple[Any, ...]]
    attempts: int


def run_agent(question: str) -> AgentOutcome:
    """Generate, execute, and judge SQL, retrying up to three attempts."""
    if not question.strip():
        raise ValueError("The question cannot be empty.")

    sql = generate_sql(question)
    feedback = ""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            result_set = execute_query(sql)
        except sqlite3.Error as error:
            feedback = (
                f"SQL execution failed: {error}\n"
                f"Failed SQL:\n{sql}"
            )
        else:
            feedback = judge(question, sql, result_set)
            if feedback == "PASS":
                return {
                    "sql": sql,
                    "result": result_set,
                    "attempts": attempt,
                }

        if attempt < MAX_ATTEMPTS:
            sql = retry(question, sql, feedback)

    raise RuntimeError(
        f"Unable to produce a correct result after {MAX_ATTEMPTS} attempts. "
        f"Last feedback: {feedback}\nLast SQL:\n{sql}"
    )


def main() -> None:
    question = input("Ask healthcare question: ")
    outcome = run_agent(question)

    print("\nSuccessful SQL:\n")
    print(outcome["sql"])
    print("\nResults:\n")
    for row in outcome["result"]:
        print(row)
    print(f"\nAccepted after {outcome['attempts']} attempt(s).")


if __name__ == "__main__":
    main()