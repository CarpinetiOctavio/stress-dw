"""Run the full reload: staging, then the dimensions and the fact table.

Run from the repository root:

    uv run python -m stress_dw.pipeline
"""

from dataclasses import dataclass
from pathlib import Path

import duckdb

from stress_dw.staging import StagingReport, run
from stress_dw.warehouse import WarehouseReport, reload_warehouse

SOURCE_PATH = Path("data/raw/mental_health.csv")
DATABASE_PATH = Path("data/stress_dw.duckdb")


@dataclass(frozen=True)
class PipelineReport:
    """The load report of each step."""

    staging: StagingReport
    warehouse: WarehouseReport


def run_pipeline(
    connection: duckdb.DuckDBPyConnection, source_path: Path
) -> PipelineReport:
    """Run the staging load, then the warehouse reload, against `source_path`."""
    staging = run(connection, source_path)
    warehouse = reload_warehouse(connection)
    return PipelineReport(staging=staging, warehouse=warehouse)


def main() -> None:
    """Fully reload `DATABASE_PATH` from `SOURCE_PATH` and print the load report."""
    with duckdb.connect(DATABASE_PATH) as connection:
        report = run_pipeline(connection, SOURCE_PATH)
    staging, warehouse = report.staging, report.warehouse
    print(f"raw rows:           {staging.raw_rows:>9,}")
    print(f"duplicates removed: {staging.duplicates_removed:>9,}")
    print(f"staged rows:        {staging.staged_rows:>9,}")
    for dimension, rows in warehouse.dimension_rows.items():
        print(f"{dimension + ':':<20}{rows:>10,}")
    print(f"{'fact_response:':<20}{warehouse.fact_rows:>10,}")
    missing = ", ".join(warehouse.missing_months) or "none"
    print(f"months with no staged record, within the staged range: {missing}")


if __name__ == "__main__":
    main()
