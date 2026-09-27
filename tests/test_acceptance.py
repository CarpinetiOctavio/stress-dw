"""Acceptance checks of docs/specification/acceptance.md, run on the real source file.

The source file is not versioned (docs/specification/staging.md#extraction);
without it at `data/raw/mental_health.csv`, these tests are skipped, not passed.
"""

from collections.abc import Iterator
from pathlib import Path

import duckdb
import pytest

from stress_dw.domains import COUNTRY_REGION, TIMESTAMP_FORMAT
from stress_dw.staging import run
from stress_dw.warehouse import reload_warehouse

SOURCE_PATH = Path(__file__).parents[1] / "data" / "raw" / "mental_health.csv"

pytestmark = pytest.mark.skipif(
    not SOURCE_PATH.exists(), reason=f"source file absent: {SOURCE_PATH}"
)


@pytest.fixture(scope="module")
def warehouse() -> Iterator[duckdb.DuckDBPyConnection]:
    with duckdb.connect() as connection:
        run(connection, SOURCE_PATH)
        reload_warehouse(connection)
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


# Natural key of each dimension (dimensions.md#row-set), and the same key
# computed directly from staging_response.
NATURAL_KEYS: dict[str, tuple[str, str]] = {
    "dim_time": (
        "year, month",
        "CAST(year(response_timestamp) AS INT), CAST(month(response_timestamp) AS INT)",
    ),
    "dim_gender": ("gender", "gender"),
    "dim_family_history": ("family_history", "family_history"),
    "dim_occupation": ("occupation", "occupation"),
    "dim_country": ("country", "country"),
    "dim_isolation": ("days_indoors", "days_indoors"),
    "dim_access": (
        "care_options, mental_health_interview",
        "care_options, mental_health_interview",
    ),
    "dim_symptoms": (
        "growing_stress, mood_swings, coping_struggles, social_weakness",
        "growing_stress, mood_swings, coping_struggles, social_weakness",
    ),
}


@pytest.mark.parametrize("dimension", NATURAL_KEYS)
def test_c1_the_dimension_is_unique_on_its_natural_key(
    warehouse: duckdb.DuckDBPyConnection, dimension: str
) -> None:
    unique_keys = warehouse.execute(
        """
        SELECT constraint_column_names FROM duckdb_constraints()
        WHERE table_name = ? AND constraint_type = 'UNIQUE'
        """,
        [dimension],
    ).fetchall()
    assert unique_keys == [(NATURAL_KEYS[dimension][0].split(", "),)]


@pytest.mark.parametrize("dimension", NATURAL_KEYS)
def test_c1_grouping_staging_by_the_natural_key_yields_the_dimension_row_set(
    warehouse: duckdb.DuckDBPyConnection, dimension: str
) -> None:
    # Identifiers only, from the fixed table above; no value is interpolated.
    key, staged_key = NATURAL_KEYS[dimension]
    grouped = f"SELECT {staged_key} FROM staging_response GROUP BY ALL"
    stored = f"SELECT {key} FROM {dimension}"
    only_in_staging = warehouse.execute(
        f"SELECT COUNT(*) FROM ({grouped} EXCEPT ALL {stored})"
    ).fetchone()
    only_in_dimension = warehouse.execute(
        f"SELECT COUNT(*) FROM ({stored} EXCEPT ALL {grouped})"
    ).fetchone()
    assert only_in_staging == (0,)
    assert only_in_dimension == (0,)


def test_c6_every_staged_country_is_in_the_mapping(
    warehouse: duckdb.DuckDBPyConnection,
) -> None:
    staged = warehouse.execute(
        "SELECT DISTINCT country FROM staging_response"
    ).fetchall()
    assert {country for (country,) in staged} <= set(COUNTRY_REGION)


def test_c6_dim_country_has_one_row_per_staged_country_at_most_35(
    warehouse: duckdb.DuckDBPyConnection,
) -> None:
    counts = warehouse.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM dim_country),
            (SELECT COUNT(DISTINCT country) FROM staging_response)
        """
    ).fetchone()
    assert counts is not None
    dimension_rows, staged_countries = counts
    assert dimension_rows == staged_countries
    assert dimension_rows <= 35
