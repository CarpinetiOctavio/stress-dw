"""Acceptance checks of docs/specification/acceptance.md, run on the real source file.

The source file is not versioned (docs/specification/staging.md#extraction);
without it at `data/raw/mental_health.csv`, these tests are skipped, not passed.
"""

from collections.abc import Iterator
from pathlib import Path

import duckdb
import pytest
from test_schema import EXPECTED_COLUMNS

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


FACT_JOINED_TO_DIMENSIONS = """
    FROM staging_response
    JOIN dim_time
        ON dim_time.year = year(staging_response.response_timestamp)
        AND dim_time.month = month(staging_response.response_timestamp)
    JOIN dim_gender USING (gender)
    JOIN dim_family_history USING (family_history)
    JOIN dim_occupation USING (occupation)
    JOIN dim_country USING (country)
    JOIN dim_isolation USING (days_indoors)
    JOIN dim_access USING (care_options, mental_health_interview)
    JOIN dim_symptoms
        USING (growing_stress, mood_swings, coping_struggles, social_weakness)
"""


def test_c2_joining_staging_to_the_eight_dimensions_multiplies_no_rows(
    warehouse: duckdb.DuckDBPyConnection,
) -> None:
    counts = warehouse.execute(
        f"""
        SELECT
            (SELECT COUNT(*) {FACT_JOINED_TO_DIMENSIONS}),
            (SELECT COUNT(*) FROM staging_response)
        """
    ).fetchone()
    assert counts == (290_051, 290_051)


def test_c3_fact_response_reconciles_with_staging(
    warehouse: duckdb.DuckDBPyConnection,
) -> None:
    counts = warehouse.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM fact_response),
            (SELECT COUNT(*) FROM staging_response),
            (SELECT COUNT(*) FROM (
                SELECT response_id FROM fact_response
                EXCEPT SELECT response_id FROM staging_response
            )),
            (SELECT COUNT(*) FROM (
                SELECT response_id FROM staging_response
                EXCEPT SELECT response_id FROM fact_response
            ))
        """
    ).fetchone()
    assert counts == (290_051, 290_051, 0, 0)


@pytest.mark.parametrize("table", EXPECTED_COLUMNS)
def test_c4_the_built_table_has_exactly_the_specified_columns_and_types(
    warehouse: duckdb.DuckDBPyConnection, table: str
) -> None:
    # The same closed list test_schema.py checks against create_schema alone,
    # checked here against the database the pipeline builds.
    columns = warehouse.execute(
        """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = ?
        ORDER BY ordinal_position
        """,
        [table],
    ).fetchall()
    assert columns == EXPECTED_COLUMNS[table]


FOREIGN_KEYS: dict[str, str] = {
    f"{dimension.removeprefix('dim_')}_id": dimension for dimension in NATURAL_KEYS
}


def test_c5_the_eight_foreign_keys_exist_with_the_specified_names(
    warehouse: duckdb.DuckDBPyConnection,
) -> None:
    foreign_keys = warehouse.execute(
        """
        SELECT constraint_column_names, referenced_table, referenced_column_names
        FROM duckdb_constraints()
        WHERE table_name = 'fact_response' AND constraint_type = 'FOREIGN KEY'
        """
    ).fetchall()
    assert sorted(foreign_keys) == sorted(
        ([column], dimension, [column]) for column, dimension in FOREIGN_KEYS.items()
    )


@pytest.mark.parametrize(("column", "dimension"), FOREIGN_KEYS.items())
def test_c5_no_fact_row_is_orphaned(
    warehouse: duckdb.DuckDBPyConnection, column: str, dimension: str
) -> None:
    # Identifiers only, from the fixed table above; no value is interpolated.
    orphans = warehouse.execute(
        f"""
        SELECT COUNT(*) FROM fact_response
        WHERE {column} NOT IN (SELECT {column} FROM {dimension})
        """
    ).fetchone()
    assert orphans == (0,)


def test_c5_the_foreign_keys_are_enforced(
    warehouse: duckdb.DuckDBPyConnection,
) -> None:
    warehouse.begin()
    try:
        with pytest.raises(duckdb.ConstraintException):
            warehouse.execute(
                """
                INSERT INTO fact_response
                SELECT MAX(response_id) + 1, -1, 1, 1, 1, 1, 1, 1, 1, 'Yes'
                FROM fact_response
                """
            )
    finally:
        warehouse.rollback()


@pytest.mark.parametrize(("column", "dimension"), FOREIGN_KEYS.items())
def test_c7_every_dimension_row_is_referenced_by_a_fact_row(
    warehouse: duckdb.DuckDBPyConnection, column: str, dimension: str
) -> None:
    # Identifiers only, from the fixed table above; no value is interpolated.
    unreferenced = warehouse.execute(
        f"""
        SELECT COUNT(*) FROM {dimension}
        WHERE {column} NOT IN (SELECT {column} FROM fact_response)
        """
    ).fetchone()
    assert unreferenced == (0,)
