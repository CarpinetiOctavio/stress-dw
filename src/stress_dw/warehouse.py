"""Reload the eight dimensions and `fact_response` from `staging_response`.

Implements step 2 of docs/specification/staging.md#load-order-and-transactions
(ADR-0010): one transaction drops the nine tables, recreates them from their
DDL, and loads the eight dimensions and then `fact_response`.
"""

from dataclasses import dataclass
from importlib.resources import files

import duckdb
import pandas as pd

from stress_dw.domains import COUNTRY_REGION, ISOLATION_LEVELS
from stress_dw.schema import TABLES, read_ddl

DIMENSIONS: tuple[str, ...] = tuple(
    table for table in TABLES if table.startswith("dim_")
)


class MappingError(ValueError):
    """A staged value has no entry in a fixed dimension mapping."""


class FactReconciliationError(ValueError):
    """`fact_response` does not hold one row per staged record (invariant I1)."""


@dataclass(frozen=True)
class WarehouseReport:
    """Row counts of the dimensions and the fact table, and months with no row.

    `missing_months` lists, as `YYYY-MM`, the calendar months between the
    earliest and the latest staged month that hold no staged record
    (docs/specification/dimensions.md#dim_time): informational, not a failure.
    """

    dimension_rows: dict[str, int]
    fact_rows: int
    missing_months: list[str]


def check_mappings(connection: duckdb.DuckDBPyConnection) -> None:
    """Abort if a staged country or isolation level is absent from its mapping.

    Implements docs/specification/country-region-mapping.md#rules for
    countries (no default region), and the same rule for `dim_isolation`'s
    fixed mapping. The load rule already restricts both columns to these
    mappings; this check names the value if that ever stops holding.

    Raises:
        MappingError: Names every unmapped value found.
    """
    unmapped: list[str] = []
    for column, mapping in (
        ("country", COUNTRY_REGION),
        ("days_indoors", ISOLATION_LEVELS),
    ):
        staged = connection.execute(
            f"SELECT DISTINCT {column} FROM staging_response ORDER BY {column}"
        ).fetchall()
        unmapped += [
            f"{column}: {value!r}" for (value,) in staged if value not in mapping
        ]
    if unmapped:
        raise MappingError(
            f"staged value(s) absent from a fixed mapping, dimension load aborted: "
            f"{'; '.join(unmapped)}"
        )


def reload_warehouse(connection: duckdb.DuckDBPyConnection) -> WarehouseReport:
    """Replace the eight dimensions and `fact_response` in one transaction.

    Assumes `staging_response` is loaded and every table in `TABLES` exists
    (see `schema.ensure_schema`). On failure the transaction is rolled back:
    the nine tables, rows and definitions alike, stay as they were.

    Raises:
        MappingError: See `check_mappings`; raised before anything is dropped.
        FactReconciliationError: `fact_response` and `staging_response` differ
            in row count after the fact load; checked before the commit.
        duckdb.Error: A statement failed, including a fact row whose foreign
            key does not resolve (invariant I3); a note on the exception
            names the table.
    """
    check_mappings(connection)
    connection.register(
        "country_region",
        pd.DataFrame(list(COUNTRY_REGION.items()), columns=["country", "region"]),
    )
    connection.register(
        "isolation_levels",
        pd.DataFrame(
            [(level, order, band) for level, (order, band) in ISOLATION_LEVELS.items()],
            columns=["days_indoors", "sort_order", "duration_band"],
        ),
    )
    connection.begin()
    table = "fact_response"
    try:
        for table in ("fact_response", *DIMENSIONS):
            connection.execute(f"DROP TABLE {table}")
        for table in (*DIMENSIONS, "fact_response"):
            connection.execute(read_ddl(table))
        for table in (*DIMENSIONS, "fact_response"):
            connection.execute(_read_load(table))
        _check_fact_reconciles(connection)
    except (duckdb.Error, FactReconciliationError) as error:
        connection.rollback()
        error.add_note(f"while reloading table {table}")
        raise
    else:
        connection.commit()
    finally:
        connection.unregister("country_region")
        connection.unregister("isolation_levels")
    return WarehouseReport(
        dimension_rows={
            dimension: _count(connection, dimension) for dimension in DIMENSIONS
        },
        fact_rows=_count(connection, "fact_response"),
        missing_months=_missing_months(connection),
    )


def _read_load(table: str) -> str:
    directory = "fact" if table == "fact_response" else "dimensions"
    return (files("stress_dw") / "sql" / directory / f"{table}.sql").read_text()


def _check_fact_reconciles(connection: duckdb.DuckDBPyConnection) -> None:
    staged = _count(connection, "staging_response")
    facts = _count(connection, "fact_response")
    if facts != staged:
        raise FactReconciliationError(
            f"fact_response holds {facts} rows for {staged} staged records; "
            f"fact load aborted"
        )


def _count(connection: duckdb.DuckDBPyConnection, table: str) -> int:
    row = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return int(row[0]) if row else 0


def _missing_months(connection: duckdb.DuckDBPyConnection) -> list[str]:
    periods = [
        period
        for (period,) in connection.execute(
            "SELECT period FROM dim_time ORDER BY period"
        ).fetchall()
    ]
    if not periods:
        return []
    calendar = pd.period_range(periods[0], periods[-1], freq="M").strftime("%Y-%m")
    present = set(periods)
    return [period for period in calendar if period not in present]
