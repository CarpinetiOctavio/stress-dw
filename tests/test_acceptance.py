"""Acceptance checks of docs/specification/acceptance.md, run on the real source file.

The source file is not versioned (docs/specification/staging.md#extraction);
without it at `data/raw/mental_health.csv`, these tests are skipped, not passed.
"""

from collections.abc import Iterator
from pathlib import Path

import duckdb
import pandas as pd
import pytest
from test_schema import EXPECTED_COLUMNS

from stress_dw.domains import COUNTRY_REGION, TIMESTAMP_FORMAT
from stress_dw.indicators import INDICATORS, IndicatorResult, run_indicator
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


STAGING_JOINED_TO_DIMENSIONS = """
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
            (SELECT COUNT(*) {STAGING_JOINED_TO_DIMENSIONS}),
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


# The two derived conditions of definitions.md, each written twice: through
# fact_response and the dimensions, as the query layer evaluates them, and
# directly against staging_response's columns, with no dimension join.
DERIVED_CONDITIONS: dict[str, tuple[str, str]] = {
    "explicit_recognition": (
        """
        SELECT fact_response.response_id
        FROM fact_response
        JOIN dim_symptoms USING (symptoms_id)
        WHERE dim_symptoms.growing_stress = 'Yes'
        """,
        """
        SELECT response_id FROM staging_response
        WHERE growing_stress = 'Yes'
        """,
    ),
    "symptom_cluster": (
        """
        SELECT fact_response.response_id
        FROM fact_response
        JOIN dim_symptoms USING (symptoms_id)
        JOIN dim_isolation USING (isolation_id)
        WHERE dim_symptoms.mood_swings IN ('Medium', 'High')
            AND dim_symptoms.coping_struggles = 'Yes'
            AND dim_isolation.days_indoors
                IN ('15-30 days', '31-60 days', 'More than 2 months')
        """,
        """
        SELECT response_id FROM staging_response
        WHERE mood_swings IN ('Medium', 'High')
            AND coping_struggles = 'Yes'
            AND days_indoors IN ('15-30 days', '31-60 days', 'More than 2 months')
        """,
    ),
}


@pytest.mark.parametrize("condition", DERIVED_CONDITIONS)
def test_c10_both_paths_count_the_same_rows(
    warehouse: duckdb.DuckDBPyConnection, condition: str
) -> None:
    """C10 as acceptance.md states it: equal row counts."""
    through_dimensions, from_staging = DERIVED_CONDITIONS[condition]
    counts = warehouse.execute(
        f"""
        SELECT
            (SELECT COUNT(*) FROM ({through_dimensions})),
            (SELECT COUNT(*) FROM ({from_staging}))
        """
    ).fetchone()
    assert counts is not None
    assert counts[0] == counts[1]


@pytest.mark.parametrize("condition", DERIVED_CONDITIONS)
def test_c10_both_paths_select_the_same_response_ids(
    warehouse: duckdb.DuckDBPyConnection, condition: str
) -> None:
    """C10, strengthened: the same set of `response_id` values, not only the same count.

    Two paths can agree on a count while selecting different rows; equal sets
    rule that out. Set equality implies the count equality acceptance.md asks
    for, which the test above checks as literally stated.
    """
    through_dimensions, from_staging = DERIVED_CONDITIONS[condition]
    differences = warehouse.execute(
        f"""
        SELECT
            (SELECT COUNT(*) FROM ({through_dimensions} EXCEPT {from_staging})),
            (SELECT COUNT(*) FROM ({from_staging} EXCEPT {through_dimensions}))
        """
    ).fetchone()
    assert differences == (0, 0)


# Each indicator's population, transcribed from indicators.md as a predicate
# over staging_response's own columns: independent of the indicator SQL,
# which evaluates it through fact_response and the dimensions.
SYMPTOM_CLUSTER_IN_STAGING = """(
    mood_swings IN ('Medium', 'High')
    AND coping_struggles = 'Yes'
    AND days_indoors IN ('15-30 days', '31-60 days', 'More than 2 months')
)"""
EXPLICIT_OR_CLUSTER_WITH_CARE_OPTIONS = (
    f"(growing_stress = 'Yes' OR {SYMPTOM_CLUSTER_IN_STAGING})"
    " AND care_options IN ('Yes', 'Not sure')"
)
POPULATIONS: dict[int, str] = dict.fromkeys(range(1, 17), "TRUE") | {
    3: "family_history = 'Yes'",
    4: "family_history = 'Yes'",
    14: SYMPTOM_CLUSTER_IN_STAGING,
    15: EXPLICIT_OR_CLUSTER_WITH_CARE_OPTIONS,
    16: EXPLICIT_OR_CLUSTER_WITH_CARE_OPTIONS,
}
# Indicators 5 and 6's condition C, over staging_response's columns.
CO_OCCURRENCE_IN_STAGING = "growing_stress = 'Yes' AND coping_struggles = 'Yes'"


def staging_count(warehouse: duckdb.DuckDBPyConnection, predicate: str) -> int:
    # `predicate` is one of the fixed transcriptions above; no value is
    # interpolated from outside this module.
    row = warehouse.execute(
        f"SELECT COUNT(*) FROM staging_response WHERE {predicate}"
    ).fetchone()
    assert row is not None
    return int(row[0])


def cells(result: IndicatorResult) -> pd.DataFrame:
    """One row per cell, with its denominator: each cell counted once."""
    keys = list(result.indicator.cuts)
    if "grouping_set" in result.rows.columns:
        keys = ["grouping_set", *keys]
    if not keys:
        # No cuts: the whole population is a single cell.
        return result.rows[["denominator"]].head(1)
    return result.rows.drop_duplicates(keys)[[*keys, "denominator"]]


@pytest.fixture(scope="module")
def indicators(
    warehouse: duckdb.DuckDBPyConnection,
) -> dict[int, IndicatorResult]:
    return {number: run_indicator(warehouse, number) for number in INDICATORS}


@pytest.mark.parametrize("number", INDICATORS)
def test_c8_cell_denominators_sum_to_the_population_counted_from_staging(
    warehouse: duckdb.DuckDBPyConnection,
    indicators: dict[int, IndicatorResult],
    number: int,
) -> None:
    population = staging_count(warehouse, POPULATIONS[number])
    denominators = cells(indicators[number])
    if "grouping_set" in denominators.columns:
        # Each grouping set partitions the population on its own.
        sums = denominators.groupby("grouping_set").denominator.sum()
        assert dict(sums) == {
            "occupation, country": population,
            "occupation, region": population,
        }
    else:
        assert denominators.denominator.sum() == population


@pytest.mark.parametrize(
    "number",
    [n for n, i in INDICATORS.items() if i.pattern in ("A", "C") and n != 8],
)
def test_c8_pattern_a_numerators_sum_to_the_cell_denominator(
    indicators: dict[int, IndicatorResult], number: int
) -> None:
    # Indicator 8 keeps only the Yes level, so its numerators cannot sum to
    # the denominator; C9 checks it against indicator 7 instead.
    result = indicators[number]
    rows = result.rows
    keys = list(result.indicator.cuts)
    if keys:
        per_cell = rows.groupby(keys).agg(
            numerators=("numerator", "sum"), denominator=("denominator", "first")
        )
        assert (per_cell.numerators == per_cell.denominator).all()
    else:
        assert rows.numerator.sum() == rows.denominator.iloc[0]


@pytest.mark.parametrize("number", [5, 6])
def test_c8_pattern_b_numerators_sum_to_the_rows_satisfying_the_condition(
    warehouse: duckdb.DuckDBPyConnection,
    indicators: dict[int, IndicatorResult],
    number: int,
) -> None:
    satisfying = staging_count(warehouse, CO_OCCURRENCE_IN_STAGING)
    sums = indicators[number].rows.groupby("grouping_set").numerator.sum()
    assert dict(sums) == {
        "occupation, country": satisfying,
        "occupation, region": satisfying,
    }


@pytest.mark.parametrize("number", [5, 6])
def test_c8_region_cells_are_sums_over_their_countries(
    indicators: dict[int, IndicatorResult], number: int
) -> None:
    rows = indicators[number].rows
    by_country = rows[rows.grouping_set == "occupation, country"].assign(
        region=lambda frame: frame.country.map(COUNTRY_REGION)
    )
    rolled_up = (
        by_country.groupby(["occupation", "region"])[["numerator", "denominator"]]
        .sum()
        .sort_index()
    )
    by_region = (
        rows[rows.grouping_set == "occupation, region"]
        .set_index(["occupation", "region"])[["numerator", "denominator"]]
        .sort_index()
    )
    pd.testing.assert_frame_equal(rolled_up, by_region)


@pytest.mark.parametrize(("count", "rate"), [(1, 2), (3, 4), (5, 6), (13, 12)])
def test_c9_the_count_indicator_equals_the_rate_indicators_numerators(
    indicators: dict[int, IndicatorResult], count: int, rate: int
) -> None:
    counted = indicators[count]
    keys = list(counted.indicator.cuts)
    if "grouping_set" in counted.rows.columns:
        keys = ["grouping_set", *keys]
    if "level" in counted.rows.columns:
        keys = [*keys, "level"]
    summed = (
        indicators[rate].rows.groupby(keys, dropna=False).numerator.sum().sort_index()
    )
    expected = counted.rows.set_index(keys).numerator.sort_index()
    pd.testing.assert_series_equal(summed, expected, check_names=False)


def test_c9_indicator_8_equals_the_yes_numerators_of_indicator_7(
    indicators: dict[int, IndicatorResult],
) -> None:
    keys = ["gender", "growing_stress"]
    rate = indicators[7].rows
    yes = rate[rate.level == "Yes"].set_index(keys).numerator.sort_index()
    count = indicators[8].rows.set_index(keys).numerator.sort_index()
    pd.testing.assert_series_equal(count, yes)


def test_c9_indicator_16_summed_over_mental_health_interview_equals_indicator_15(
    indicators: dict[int, IndicatorResult],
) -> None:
    keys = ["growing_stress", "symptom_cluster", "care_options"]
    full = indicators[16]
    numerators = full.rows.groupby([*keys, "level"]).numerator.sum().sort_index()
    denominators = cells(full).groupby(keys).denominator.sum().sort_index()
    fifteen = indicators[15]
    pd.testing.assert_series_equal(
        numerators,
        fifteen.rows.set_index([*keys, "level"]).numerator.sort_index(),
    )
    pd.testing.assert_series_equal(
        denominators,
        cells(fifteen).set_index(keys).denominator.sort_index(),
    )
