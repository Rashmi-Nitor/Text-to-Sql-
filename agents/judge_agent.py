import re
from typing import Any

from src.llm_client import generate


JUDGE_SYSTEM_PROMPT = (
    "You are a business-correctness judge for healthcare SQL. "
    "Decide whether the result set answers the user's question, not merely "
    "whether the SQL is syntactically valid. Reply with PASS or FAIL followed "
    "by a concise reason. Only use PASS when the result is responsive to the "
    "question."
)


def judge(question: str, sql: str, result_set: list[tuple[Any, ...]]) -> str:
    """Return PASS or a FAIL verdict with a reason for an incorrect result."""
    prompt = (
        f"Question:\n{question}\n\n"
        f"Generated SQL:\n{sql}\n\n"
        f"Result set:\n{result_set!r}\n\n"
        "Does this result answer the question correctly?"
    )
    response = generate(prompt, system_prompt=JUDGE_SYSTEM_PROMPT).strip()
    match = re.match(r"^(PASS|FAIL)\b", response, re.IGNORECASE)
    if match is None:
        raise RuntimeError(
            "The judge returned an invalid verdict; expected PASS or FAIL."
        )

    if match.group(1).upper() == "PASS":
        return "PASS"
    return f"FAIL: {response[match.end():].strip(' :-')}".rstrip()