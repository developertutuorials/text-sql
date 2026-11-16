"""Build the schema-aware prompt sent to the LLM."""

TEMPLATE = """You are a SQLite expert. Write a single SQL SELECT query that answers
the question. Return only the SQL, no explanation.

Schema:
{schema}

Question: {question}
SQL:"""


def build(schema: str, question: str) -> str:
    return TEMPLATE.format(schema=schema, question=question)
