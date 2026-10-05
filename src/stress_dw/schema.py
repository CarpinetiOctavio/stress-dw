"""Create the star schema: `staging_response`, the eight dimensions, `fact_response`.

Each table's DDL lives in its own file under `sql/schema/`, transcribed from
docs/specification/staging.md, dimensions.md, and fact-table.md.

Every column in the schema is NOT NULL. Primary keys are NOT NULL by
definition, and fact-table.md specifies NOT NULL on `fact_response`'s foreign
keys and `treatment`. The remaining columns rest on two grounds, by kind:

* Columns holding a source value (`staging_response`'s thirteen modeled
  columns, and each dimension's natural key): the load rule in
  docs/specification/sources.md#load-rule already aborts the load on a NULL
  in any modeled column, which sustains invariant I1
  (docs/specification/fact-table.md#invariants). NOT NULL is not a new
  requirement; it is the same rule enforced a second time, by the engine,
  beneath the load rule that the Python load step enforces
  (`staging.enforce_load_rule`). The second layer
  matters because DuckDB's UNIQUE does not reject NULL: a UNIQUE column
  accepted two NULL rows without error, checked against DuckDB 1.5.5. Without
  NOT NULL, a natural key such as `dim_gender.gender` could hold a NULL
  through a defect in the load rule, and the engine would raise nothing. This
  applies the principle of ADR-0009's first decision driver (enforcement the
  engine performs, not enforcement the application must remember) to NULL;
  that extension is this project's own interpretation, not part of what
  ADR-0009 decided.
* Derived dimension columns (`dim_country.region`, `dim_isolation.sort_order`
  and `duration_band`, and `dim_time`'s `month_name`, `period`, `quarter`,
  `semester`): the load rule does not cover them. `region` has no default
  (docs/specification/country-region-mapping.md#rules: a staged country
  absent from the mapping aborts the load); the others are fixed mappings or
  functions of `month`, defined for every value of their natural key. A NULL
  in any of them can only come from a pipeline defect.
"""

from collections.abc import Sequence
from importlib.resources import files

import duckdb

# Creation order: `fact_response` last, since its foreign keys reference the
# eight dimensions.
TABLES: tuple[str, ...] = (
    "staging_response",
    "dim_time",
    "dim_gender",
    "dim_family_history",
    "dim_occupation",
    "dim_country",
    "dim_isolation",
    "dim_access",
    "dim_symptoms",
    "fact_response",
)


def read_ddl(table: str) -> str:
    """Return the CREATE TABLE statement for `table` from `sql/schema/`."""
    return (files("stress_dw") / "sql" / "schema" / f"{table}.sql").read_text()


def create_schema(connection: duckdb.DuckDBPyConnection) -> None:
    """Create every table in `TABLES`, in order, in one transaction.

    Assumes none of the tables exists yet. If any statement fails, the
    transaction is rolled back and no table is left behind.

    Raises:
        duckdb.Error: A CREATE TABLE statement failed; a note on the exception
            names the table.
    """
    _create_tables(connection, TABLES)


def ensure_schema(connection: duckdb.DuckDBPyConnection) -> None:
    """Create the tables in `TABLES` that do not exist yet, in one transaction.

    Lets the full reload of docs/specification/staging.md#update-policy run
    against a database a previous run already created. An existing table is
    left as it is; its definition is not compared against its DDL file.

    Raises:
        duckdb.Error: A CREATE TABLE statement failed; a note on the exception
            names the table.
    """
    existing = {
        name
        for (name,) in connection.execute(
            "SELECT table_name FROM information_schema.tables"
        ).fetchall()
    }
    _create_tables(connection, [table for table in TABLES if table not in existing])


def _create_tables(
    connection: duckdb.DuckDBPyConnection, tables: Sequence[str]
) -> None:
    connection.begin()
    for table in tables:
        try:
            connection.execute(read_ddl(table))
        except duckdb.Error as error:
            connection.rollback()
            error.add_note(f"while creating table {table}")
            raise
    connection.commit()
