# Code conventions (Python & SQL)

Extends the [model conventions](specification/definitions.md#model-conventions) already fixed in the specification into the code that implements it. For prose, comments included, see [`writing-conventions.md`](writing-conventions.md).

## 1. Python version and tooling

- Python 3.12+.
- `ruff` for both linting and formatting (`ruff check`, `ruff format`) — one tool, not black/flake8/isort/pyupgrade separately. Configuration lives in `pyproject.toml`.
- `mypy --strict`. A `# type: ignore[<code>]` is allowed only with a comment naming why — typically an incomplete pandas or mysql.connector stub — never a blanket ignore.
- Dependencies declared in `pyproject.toml`, managed with `uv`. No `requirements.txt`.

## 2. Naming

- Anything naming a database object follows the [model conventions](specification/definitions.md#model-conventions) exactly: a Python identifier referring to `dim_time`, `fact_response`, or a column never renames or abbreviates it.
- Everything else follows standard Python convention: `snake_case` for functions and variables, `UPPER_SNAKE_CASE` for constants, `PascalCase` for classes.

## 3. Docstrings

- Google style. Every public function, class, and module has one; a one-line docstring is enough when the name and signature are already self-explanatory.
- A docstring states what a function does and what it assumes about its inputs — for example, that a DataFrame has already passed the [load rule](specification/sources.md#load-rule) — not a restatement of the type hints already in the signature.

## 4. Testing

- `pytest`. One test module per source module, named `test_<module>.py`.
- Every acceptance check in [`acceptance.md`](specification/acceptance.md) (C1 through C10) is an automated test, not a query run and recorded by hand — the checks need to be re-run on every load, and Fase 4's update policy will need that repeatability once it's specified.
- A test's name states the behavior it checks, not the function under test: `test_orphan_fact_rows_are_zero`, not `test_load_facts`.

## 5. SQL

- Keywords uppercase, identifiers lowercase. Identifiers follow the [model conventions](specification/definitions.md#model-conventions) already fixed there — not restated here.
- SQL lives in `.sql` files, one statement or one logical step per file, not built as Python string concatenation. A parameterized query only — never a value interpolated directly into a query string.

## 6. Error handling

- Extends the [load rule](specification/sources.md#load-rule): a value outside its documented domain aborts the load; it is never coerced or defaulted silently.
- No bare `except:`. Every caught exception is a named type, and its message includes whatever identifies the row or step that failed, so a failure traces back to an [acceptance check](specification/acceptance.md) or an [invariant](specification/fact-table.md#invariants).
