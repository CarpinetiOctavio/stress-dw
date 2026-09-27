"""Acceptance checks of docs/specification/acceptance.md, run on the real source file.

The source file is not versioned (docs/specification/staging.md#extraction);
without it at `data/raw/mental_health.csv`, these tests are skipped, not passed.
"""

from collections.abc import Iterator
from pathlib import Path

import duckdb
import pytest

from stress_dw.domains import TIMESTAMP_FORMAT
from stress_dw.staging import run

SOURCE_PATH = Path(__file__).parents[1] / "data" / "raw" / "mental_health.csv"

pytestmark = pytest.mark.skipif(
    not SOURCE_PATH.exists(), reason=f"source file absent: {SOURCE_PATH}"
)


@pytest.fixture(scope="module")
def warehouse() -> Iterator[duckdb.DuckDBPyConnection]:
    with duckdb.connect() as connection:
        run(connection, SOURCE_PATH)
        connection.execute(
            "CREATE TABLE raw_source AS SELECT * FROM read_csv(?, all_varchar = true)",
            [str(SOURCE_PATH)],
        )
        yield connection


def test_c11_staging_holds_290051_rows(warehouse: duckdb.DuckDBPyConnection) -> None:
    count = warehouse.execute("SELECT COUNT(*) FROM staging_response").fetchone()
    assert count == (290_051,)


# DuckDB's own reading of the source file, collapsed with SELECT DISTINCT over
# all 17 columns and projected onto the 13 modeled ones: independent of
# staging.py. The single parameter is the `Timestamp` format.
DISTINCT_SOURCE_ROWS = """
    SELECT
        strptime("Timestamp", ?), "Gender", "Country", "Occupation",
        "family_history", "treatment", "Days_Indoors", "Growing_Stress",
        "Mood_Swings", "Coping_Struggles", "Social_Weakness",
        "mental_health_interview", "care_options"
    FROM (SELECT DISTINCT * FROM raw_source)
"""

STAGING_ROWS = """
    SELECT
        response_timestamp, gender, country, occupation,
        family_history, treatment, days_indoors, growing_stress,
        mood_swings, coping_struggles, social_weakness,
        mental_health_interview, care_options
    FROM staging_response
"""


def test_c11_the_source_file_has_292364_rows_and_290051_distinct_ones(
    warehouse: duckdb.DuckDBPyConnection,
) -> None:
    counts = warehouse.execute(
        """
        SELECT COUNT(*), (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM raw_source))
        FROM raw_source
        """
    ).fetchone()
    assert counts == (292_364, 290_051)


def test_c11_every_removed_row_is_a_17_column_duplicate_of_a_kept_row(
    warehouse: duckdb.DuckDBPyConnection,
) -> None:
    # If staging removed a row that is not an exact 17-column duplicate, or
    # kept one that is, the two multisets differ in one direction or the other.
    only_in_source = warehouse.execute(
        f"SELECT COUNT(*) FROM ({DISTINCT_SOURCE_ROWS} EXCEPT ALL {STAGING_ROWS})",
        [TIMESTAMP_FORMAT],
    ).fetchone()
    only_in_staging = warehouse.execute(
        f"SELECT COUNT(*) FROM ({STAGING_ROWS} EXCEPT ALL {DISTINCT_SOURCE_ROWS})",
        [TIMESTAMP_FORMAT],
    ).fetchone()
    assert only_in_source == (0,)
    assert only_in_staging == (0,)
