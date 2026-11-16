"""Create a small sample SQLite database."""
import sqlite3

DB = "sample.db"

SCHEMA = """
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, country TEXT);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    amount REAL,
    created_at TEXT
);
"""

ROWS = {
    "customers": [
        (1, "Asha", "IN"),
        (2, "Ben", "US"),
        (3, "Chen", "IN"),
    ],
    "orders": [
        (1, 1, 250.0, "2026-01-05"),
        (2, 1, 120.0, "2026-02-11"),
        (3, 2, 90.0, "2026-01-20"),
        (4, 3, 400.0, "2026-03-02"),
    ],
}


def build(path: str = DB) -> None:
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    conn.executemany("INSERT INTO customers VALUES (?,?,?)", ROWS["customers"])
    conn.executemany("INSERT INTO orders VALUES (?,?,?,?)", ROWS["orders"])
    conn.commit()
    conn.close()
    print(f"built {path}")


if __name__ == "__main__":
    import os

    if os.path.exists(DB):
        os.remove(DB)
    build()
