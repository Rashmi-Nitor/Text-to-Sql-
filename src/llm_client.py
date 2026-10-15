import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

SQL_SYSTEM_PROMPT = (
    "Return exactly one valid SQLite SELECT statement. "
    "Do not include reasoning, explanations, or Markdown."
)


def generate(prompt: str, system_prompt: str = SQL_SYSTEM_PROMPT) -> str:
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key or not api_key.strip():
        raise ValueError(
            "NVIDIA_API_KEY is missing. Set it in the project's .env file or "
            "in your environment before running the application."
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://integrate.api.nvidia.com/v1"
    )
    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-lightning-30b-a3b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=1024,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False,
                "force_nonempty_content": True
            }
        }
    )

    if not response.choices:
        raise RuntimeError("The model returned no completion choices.")

    content = response.choices[0].message.content
    if content is None or not content.strip():
        raise RuntimeError("The model returned an empty response instead of SQL.")

    return content