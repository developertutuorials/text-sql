"""LLM client. Uses OpenAI when a key is present; otherwise returns a canned
query so the pipeline runs offline."""
import os

MOCK_SQL = "SELECT country, COUNT(*) AS n FROM customers GROUP BY country;"


def generate_sql(prompt: str) -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return MOCK_SQL
    from openai import OpenAI

    client = OpenAI(api_key=key)
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return _strip(resp.choices[0].message.content)


def _strip(text: str) -> str:
    """Remove markdown fences the model sometimes adds."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    return text.strip()
