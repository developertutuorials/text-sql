import sqlite3

import pytest

from src.agent import is_read_only, run
from src.db import ROWS, SCHEMA
from src.prompt import build
from src.schema import describe


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    c.executemany("INSERT INTO customers VALUES (?,?,?)", ROWS["customers"])
    c.executemany("INSERT INTO orders VALUES (?,?,?,?)", ROWS["orders"])
    yield c
    c.close()


def test_schema_lists_both_tables(conn):
    desc = describe(conn)
    assert "customers(" in desc and "orders(" in desc


def test_prompt_embeds_schema_and_question():
    p = build("customers(id INTEGER)", "how many customers?")
    assert "customers(id INTEGER)" in p and "how many customers?" in p


def test_read_only_guard():
    assert is_read_only("SELECT * FROM customers")
    assert not is_read_only("DELETE FROM customers")
    assert not is_read_only("SELECT 1; DROP TABLE customers")


def test_run_returns_rows(conn):
    # no API key in CI -> mock SQL groups customers by country
    sql, rows = run(conn, "customers per country")
    assert sql.lower().startswith("select")
    assert dict(rows) == {"IN": 2, "US": 1}
