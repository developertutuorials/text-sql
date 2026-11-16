# text-to-sql-assistant

Turns natural-language questions into SQL. Reads the database schema, prompts an
LLM to write a query, runs it against SQLite, and returns the rows.

## Stack
Python, SQLite, pluggable LLM client.

## Layout
```
src/
  db.py       build a sample SQLite database
  schema.py   introspect tables and columns
  prompt.py   build the schema-aware prompt
  llm.py      LLM client; mock fallback when no API key is set
  agent.py    question -> SQL -> results (with a read-only safety check)
app.py        command-line loop
tests/        schema + prompt + safety tests
```

## Run
```bash
pip install -r requirements.txt
python -m src.db          # creates sample.db
python app.py             # ask questions in natural language
```

Set an OpenAI-compatible key for real SQL generation; without one the assistant
returns a canned example query so the flow still runs:
```bash
export OPENAI_API_KEY=...
```

## Safety
Only `SELECT` statements are executed. Anything else is rejected before it reaches
the database.

## Tests
```bash
pytest
```
