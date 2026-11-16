"""Introspect a SQLite schema into a compact text description for the prompt."""
import sqlite3


def describe(conn: sqlite3.Connection) -> str:
    tables = [
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
    ]
    lines = []
    for t in tables:
        cols = [f"{c[1]} {c[2]}" for c in conn.execute(f"PRAGMA table_info({t})")]
        lines.append(f"{t}({', '.join(cols)})")
    return "\n".join(lines)
