from collections.abc import Iterator
from datetime import datetime

import duckdb
import pytest

from stress_dw import warehouse
from stress_dw.schema import TABLES, create_schema
from stress_dw.warehouse import (
    DIMENSIONS,
    FactReconciliationError,
    MappingError,
    reload_warehouse,
)

# A valid staged record, by `staging_response` column, `response_id` excluded.
VALID_RECORD: dict[str, object] = {
    "response_timestamp": datetime(2014, 8, 27, 11, 29),
    "gender": "Female",
    "country": "United States",
    "occupation": "Corporate",
    "family_history": "No",
    "treatment": "Yes",
    "days_indoors": "1-14 days",
    "growing_stress": "Yes",
    "mood_swings": "Medium",
    "coping_struggles": "No",
    "social_weakness": "Yes",
    "mental_health_interview": "No",
    "care_options": "Not sure",
}

INSERT_STAGED = f"INSERT INTO staging_response VALUES ({', '.join(['?'] * 14)})"


def stage(connection: duckdb.DuckDBPyConnection, *records: dict[str, object]) -> None:
    for response_id, overrides in enumerate(records, start=1):
        record = VALID_RECORD | overrides
        connection.execute(INSERT_STAGED, [response_id, *record.values()])


def rows(connection: duckdb.DuckDBPyConnection, table: str) -> list[tuple[object, ...]]:
    return connection.execute(f"SELECT * FROM {table} ORDER BY 1").fetchall()


def snapshot(
    connection: duckdb.DuckDBPyConnection,
) -> dict[str, list[tuple[object, ...]]]:
    return {table: rows(connection, table) for table in (*DIMENSIONS, "fact_response")}


@pytest.fixture
def connection() -> Iterator[duckdb.DuckDBPyConnection]:
    with duckdb.connect() as connection:
        create_schema(connection)
        yield connection


def test_each_dimension_holds_one_row_per_distinct_natural_key(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    stage(connection, {}, {"gender": "Male"}, {}, {"gender": "Male"})
    report = reload_warehouse(connection)
    assert rows(connection, "dim_gender") == [(1, "Female"), (2, "Male")]
    assert report.dimension_rows == dict.fromkeys(DIMENSIONS, 1) | {"dim_gender": 2}
    assert report.fact_rows == 4


def test_surrogate_keys_follow_natural_key_order(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    stage(connection, {"occupation": "Student"}, {"occupation": "Business"})
    reload_warehouse(connection)
    assert rows(connection, "dim_occupation") == [(1, "Business"), (2, "Student")]


@pytest.mark.parametrize(
    ("month", "month_name", "period", "quarter", "semester"),
    [
        (1, "January", "2015-01", 1, 1),
        (3, "March", "2015-03", 1, 1),
        (4, "April", "2015-04", 2, 1),
        (6, "June", "2015-06", 2, 1),
        (7, "July", "2015-07", 3, 2),
        (10, "October", "2015-10", 4, 2),
        (12, "December", "2015-12", 4, 2),
    ],
)
def test_dim_time_derives_its_columns_from_year_and_month(
    connection: duckdb.DuckDBPyConnection,
    month: int,
    month_name: str,
    period: str,
    quarter: int,
    semester: int,
) -> None:
    stage(connection, {"response_timestamp": datetime(2015, month, 15, 9, 0)})
    reload_warehouse(connection)
    assert rows(connection, "dim_time") == [
        (1, 2015, month, month_name, period, quarter, semester)
    ]


def test_dim_country_takes_its_region_from_the_fixed_mapping(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    stage(connection, {"country": "Mexico"}, {"country": "Georgia"})
    reload_warehouse(connection)
    assert rows(connection, "dim_country") == [
        (1, "Georgia", "Asia"),
        (2, "Mexico", "Latin America and the Caribbean"),
    ]


def test_dim_isolation_takes_sort_order_and_band_from_the_fixed_mapping(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    stage(
        connection,
        {"days_indoors": "Go out Every day"},
        {"days_indoors": "15-30 days"},
        {"days_indoors": "More than 2 months"},
    )
    reload_warehouse(connection)
    assert rows(connection, "dim_isolation") == [
        (1, "15-30 days", 3, "Medium"),
        (2, "Go out Every day", 1, "Low"),
        (3, "More than 2 months", 5, "High"),
    ]


def test_the_report_lists_months_with_no_staged_record_within_the_range(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    stage(
        connection,
        {"response_timestamp": datetime(2014, 11, 1, 0, 0)},
        {"response_timestamp": datetime(2015, 2, 1, 0, 0)},
    )
    report = reload_warehouse(connection)
    assert report.missing_months == ["2014-12", "2015-01"]


def test_a_staged_country_absent_from_the_mapping_aborts_before_any_drop(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    stage(connection, {})
    reload_warehouse(connection)
    before = snapshot(connection)
    connection.execute("UPDATE staging_response SET country = 'Atlantis'")
    with pytest.raises(MappingError, match="country: 'Atlantis'"):
        reload_warehouse(connection)
    assert snapshot(connection) == before


def test_a_reload_succeeds_while_fact_rows_reference_every_dimension(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    # ADR-0010, Confirmation: the second run's case, which per-table
    # transactions cannot handle under DuckDB (ADR-0009, E3).
    stage(connection, {})
    reload_warehouse(connection)
    assert len(rows(connection, "fact_response")) == 1
    connection.execute("UPDATE staging_response SET gender = 'Male'")
    reload_warehouse(connection)
    assert rows(connection, "dim_gender") == [(1, "Male")]
    assert rows(connection, "fact_response") == [(1, 1, 1, 1, 1, 1, 1, 1, 1, "Yes")]


def test_a_failure_inside_the_reload_leaves_the_nine_tables_as_they_were(
    connection: duckdb.DuckDBPyConnection, monkeypatch: pytest.MonkeyPatch
) -> None:
    # ADR-0010, Confirmation: a failure forced after the drops, the
    # recreation, and all but the last dimension load.
    stage(connection, {})
    reload_warehouse(connection)
    before = snapshot(connection)
    assert len(before["fact_response"]) == 1
    read_load = warehouse._read_load

    def fail_on_last_dimension(dimension: str) -> str:
        if dimension == DIMENSIONS[-1]:
            return "SELECT * FROM table_that_does_not_exist"
        return read_load(dimension)

    monkeypatch.setattr(warehouse, "_read_load", fail_on_last_dimension)
    connection.execute("UPDATE staging_response SET gender = 'Male'")
    with pytest.raises(duckdb.CatalogException) as raised:
        reload_warehouse(connection)
    foreign_keys = connection.execute(
        """
        SELECT COUNT(*) FROM duckdb_constraints()
        WHERE table_name = 'fact_response' AND constraint_type = 'FOREIGN KEY'
        """
    ).fetchone()
    tables = connection.execute(
        "SELECT table_name FROM information_schema.tables"
    ).fetchall()
    assert snapshot(connection) == before
    assert foreign_keys == (8,)
    assert sorted(name for (name,) in tables) == sorted(TABLES)
    assert f"while reloading table {DIMENSIONS[-1]}" in raised.value.__notes__


def test_each_staged_record_becomes_one_fact_row_with_its_dimension_keys(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    stage(
        connection,
        {"gender": "Male", "treatment": "No"},
        {"country": "Brazil", "response_timestamp": datetime(2015, 2, 1, 0, 0)},
    )
    reload_warehouse(connection)
    facts = connection.execute(
        """
        SELECT
            fact_response.response_id, dim_time.period, dim_gender.gender,
            dim_country.country, fact_response.treatment
        FROM fact_response
        JOIN dim_time USING (time_id)
        JOIN dim_gender USING (gender_id)
        JOIN dim_country USING (country_id)
        ORDER BY fact_response.response_id
        """
    ).fetchall()
    assert facts == [
        (1, "2014-08", "Male", "United States", "No"),
        (2, "2015-02", "Female", "Brazil", "Yes"),
    ]


def test_the_fact_load_copies_response_id_from_staging(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    stage(connection, {}, {})
    connection.execute("UPDATE staging_response SET response_id = response_id + 100")
    reload_warehouse(connection)
    ids = connection.execute(
        "SELECT response_id FROM fact_response ORDER BY 1"
    ).fetchall()
    assert ids == [(101,), (102,)]


def test_an_unresolved_foreign_key_aborts_and_leaves_the_nine_tables_as_they_were(
    connection: duckdb.DuckDBPyConnection, monkeypatch: pytest.MonkeyPatch
) -> None:
    # dim_gender is left empty, so every staged record's gender_id is NULL.
    stage(connection, {})
    reload_warehouse(connection)
    before = snapshot(connection)
    read_load = warehouse._read_load

    def empty_dim_gender(table: str) -> str:
        return "SELECT 1" if table == "dim_gender" else read_load(table)

    monkeypatch.setattr(warehouse, "_read_load", empty_dim_gender)
    with pytest.raises(duckdb.ConstraintException) as raised:
        reload_warehouse(connection)
    assert snapshot(connection) == before
    assert "while reloading table fact_response" in raised.value.__notes__


def test_a_fact_row_count_differing_from_staging_aborts_before_commit(
    connection: duckdb.DuckDBPyConnection, monkeypatch: pytest.MonkeyPatch
) -> None:
    stage(connection, {}, {})
    reload_warehouse(connection)
    before = snapshot(connection)
    read_load = warehouse._read_load

    def skip_fact_load(table: str) -> str:
        return "SELECT 1" if table == "fact_response" else read_load(table)

    monkeypatch.setattr(warehouse, "_read_load", skip_fact_load)
    with pytest.raises(FactReconciliationError, match="0 rows for 2 staged"):
        reload_warehouse(connection)
    assert snapshot(connection) == before
