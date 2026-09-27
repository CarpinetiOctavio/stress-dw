"""Reload the eight dimensions and `fact_response` from `staging_response`.

Implements step 2 of docs/specification/staging.md#load-order-and-transactions
(ADR-0010): one transaction drops the nine tables, recreates them from their
DDL, and loads them. The fact load is not implemented yet; `fact_response` is
recreated empty.
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


@dataclass(frozen=True)
class WarehouseReport:
    """Row count of each dimension, and the months `dim_time` has no row for.

    `missing_months` lists, as `YYYY-MM`, the calendar months between the
    earliest and the latest staged month that hold no staged record
    (docs/specification/dimensions.md#dim_time): informational, not a failure.
    """

    dimension_rows: dict[str, int]
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
        duckdb.Error: A statement failed; a note on the exception names the
            table.
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
        for table in DIMENSIONS:
            connection.execute(_read_load(table))
    except duckdb.Error as error:
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
        missing_months=_missing_months(connection),
    )


def _read_load(dimension: str) -> str:
    return (files("stress_dw") / "sql" / "dimensions" / f"{dimension}.sql").read_text()


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
