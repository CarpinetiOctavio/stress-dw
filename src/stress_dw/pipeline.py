"""Run the full reload: staging, then the dimensions and the fact table.

Run from the repository root:

    uv run python -m stress_dw.pipeline
"""

from pathlib import Path

import duckdb

from stress_dw.staging import run
from stress_dw.warehouse import reload_warehouse

SOURCE_PATH = Path("data/raw/mental_health.csv")
DATABASE_PATH = Path("data/stress_dw.duckdb")


def main() -> None:
    """Fully reload `DATABASE_PATH` from `SOURCE_PATH` and print the load report."""
    with duckdb.connect(DATABASE_PATH) as connection:
        staging = run(connection, SOURCE_PATH)
        warehouse = reload_warehouse(connection)
    print(f"raw rows:           {staging.raw_rows:>9,}")
    print(f"duplicates removed: {staging.duplicates_removed:>9,}")
    print(f"staged rows:        {staging.staged_rows:>9,}")
    for dimension, rows in warehouse.dimension_rows.items():
        print(f"{dimension + ':':<20}{rows:>10,}")
    missing = ", ".join(warehouse.missing_months) or "none"
    print(f"months with no staged record, within the staged range: {missing}")


if __name__ == "__main__":
    main()
