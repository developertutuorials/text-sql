"""Question -> SQL -> results, with a read-only guard."""
import sqlite3

from . import llm
from .prompt import build
from .schema import describe


def is_read_only(sql: str) -> bool:
    """Allow a single SELECT; reject writes and statement stacking."""
    s = sql.strip().rstrip(";").lower()
    if ";" in s:
        return False
    return s.startswith("select") or s.startswith("with")


def run(conn: sqlite3.Connection, question: str) -> tuple[str, list]:
    prompt = build(describe(conn), question)
    sql = llm.generate_sql(prompt)
    if not is_read_only(sql):
        raise ValueError(f"refusing to run non-SELECT query: {sql}")
    rows = conn.execute(sql).fetchall()
    return sql, rows
