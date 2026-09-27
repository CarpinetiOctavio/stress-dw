from collections.abc import Iterator
from datetime import datetime

import duckdb
import pytest
from test_warehouse import stage

from stress_dw.indicators import (
    INDICATORS,
    SYMPTOM_CLUSTER_CAVEAT,
    run_indicator,
)
from stress_dw.schema import create_schema
from stress_dw.warehouse import reload_warehouse


@pytest.fixture
def connection() -> Iterator[duckdb.DuckDBPyConnection]:
    with duckdb.connect() as connection:
        create_schema(connection)
        yield connection


def load(connection: duckdb.DuckDBPyConnection, *records: dict[str, object]) -> None:
    stage(connection, *records)
    reload_warehouse(connection)


def test_a_level_absent_from_a_cell_is_reported_with_numerator_zero(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    load(
        connection,
        {"gender": "Female", "growing_stress": "Yes"},
        {"gender": "Male", "growing_stress": "No"},
    )
    rows = run_indicator(connection, 2).rows
    female_no = rows[(rows.gender == "Female") & (rows.level == "No")]
    assert list(female_no.numerator) == [0]
    assert list(female_no.rate) == [0.0]


def test_pattern_a_numerators_sum_to_the_denominator_within_each_cell(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    load(
        connection,
        {"growing_stress": "Yes"},
        {"growing_stress": "No"},
        {"growing_stress": "Maybe"},
        {"growing_stress": "Yes", "gender": "Male"},
    )
    rows = run_indicator(connection, 2).rows
    per_cell = rows.groupby(["period", "gender"]).agg(
        numerators=("numerator", "sum"), denominator=("denominator", "first")
    )
    assert (per_cell.numerators == per_cell.denominator).all()
    assert list(per_cell.denominator) == [3, 1]


def test_rate_is_numerator_over_denominator(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    load(connection, {"treatment": "Yes"}, {"treatment": "No"}, {"treatment": "No"})
    rows = run_indicator(connection, 7).rows.set_index("level")
    assert rows.loc["No", "rate"] == pytest.approx(2 / 3)
    assert rows.loc["Yes", "rate"] == pytest.approx(1 / 3)


@pytest.mark.parametrize(("threshold", "low_n"), [(3, False), (4, True)])
def test_low_n_flags_a_denominator_strictly_below_the_threshold(
    connection: duckdb.DuckDBPyConnection, threshold: int, low_n: bool
) -> None:
    load(connection, {}, {}, {})
    rows = run_indicator(connection, 1, low_n_threshold=threshold).rows
    assert set(rows.denominator) == {3}
    assert set(rows.low_n) == {low_n}


def test_the_default_low_n_threshold_is_30(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    load(connection, *[{}] * 30)
    assert not run_indicator(connection, 1).rows.low_n.any()


def test_indicator_5_reports_both_grouping_sets_and_rolls_countries_up_to_region(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    both: dict[str, object] = {"growing_stress": "Yes", "coping_struggles": "Yes"}
    load(
        connection,
        both | {"country": "United States"},
        {"country": "United States"},
        both | {"country": "Canada"},
    )
    rows = run_indicator(connection, 5).rows
    by_country = rows[rows.grouping_set == "occupation, country"]
    by_region = rows[rows.grouping_set == "occupation, region"]
    assert by_country.region.isna().all()
    assert by_region.country.isna().all()
    assert sorted(zip(by_country.country, by_country.numerator, strict=True)) == [
        ("Canada", 1),
        ("United States", 1),
    ]
    assert list(
        zip(by_region.region, by_region.numerator, by_region.denominator, strict=True)
    ) == [("Northern America", 2, 3)]


def test_indicator_10_carries_the_medium_plus_high_headline_rate(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    load(
        connection,
        {"mood_swings": "Low"},
        {"mood_swings": "Medium"},
        {"mood_swings": "High"},
        {"mood_swings": "High"},
    )
    rows = run_indicator(connection, 10).rows
    assert list(rows.headline_rate.unique()) == pytest.approx([3 / 4])
    assert rows.numerator.sum() == 4


def test_indicator_8_keeps_only_the_yes_level(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    load(connection, {"treatment": "Yes"}, {"treatment": "No"})
    rows = run_indicator(connection, 8).rows
    assert list(rows.level) == ["Yes"]
    assert list(rows.denominator) == [2]


def test_indicator_15_excludes_rows_outside_its_population(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    load(
        connection,
        {"growing_stress": "Yes", "care_options": "Yes"},
        {"growing_stress": "Yes", "care_options": "No"},
        {"growing_stress": "No", "care_options": "Yes"},
        {
            "growing_stress": "No",
            "care_options": "Not sure",
            "mood_swings": "High",
            "coping_struggles": "Yes",
            "days_indoors": "31-60 days",
        },
    )
    rows = run_indicator(connection, 15).rows
    cells = rows.drop_duplicates(["growing_stress", "symptom_cluster", "care_options"])
    assert sorted(
        zip(
            cells.growing_stress, cells.symptom_cluster, cells.care_options, strict=True
        )
    ) == [("No", True, "Not sure"), ("Yes", False, "Yes")]


def test_months_are_reported_as_period(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    load(connection, {"response_timestamp": datetime(2015, 2, 3, 4, 5)})
    assert set(run_indicator(connection, 2).rows.period) == {"2015-02"}


@pytest.mark.parametrize("number", INDICATORS)
def test_only_indicators_using_symptom_cluster_carry_its_caveat(
    connection: duckdb.DuckDBPyConnection, number: int
) -> None:
    load(connection, {})
    caveats = run_indicator(connection, number).caveats
    expected = (SYMPTOM_CLUSTER_CAVEAT,) if number in (14, 15, 16) else ()
    assert caveats == expected


@pytest.mark.parametrize("number", [0, 17])
def test_an_unknown_indicator_number_is_rejected(
    connection: duckdb.DuckDBPyConnection, number: int
) -> None:
    with pytest.raises(ValueError, match=f"no indicator {number}"):
        run_indicator(connection, number)
