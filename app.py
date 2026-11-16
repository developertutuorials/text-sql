"""CLI: ask questions in natural language against sample.db."""
import os
import sqlite3
import sys

from src.agent import run
from src.db import DB, build


def main() -> None:
    if not os.path.exists(DB):
        build()
    conn = sqlite3.connect(DB)
    print("Ask a question about customers/orders (Ctrl-C to quit).")
    try:
        while True:
            q = input("\n> ").strip()
            if not q:
                continue
            sql, rows = run(conn, q)
            print(f"SQL: {sql}")
            for r in rows:
                print(r)
    except (KeyboardInterrupt, EOFError):
        print()
    except ValueError as e:
        print(e, file=sys.stderr)


if __name__ == "__main__":
    main()
