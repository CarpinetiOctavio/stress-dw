from collections.abc import Iterator
from pathlib import Path

import duckdb
import pandas as pd
import pytest

from stress_dw import staging
from stress_dw.schema import create_schema
from stress_dw.staging import (
    SOURCE_COLUMNS,
    LoadRuleError,
    SourceChecksumError,
    SourceHeaderError,
    clean,
    deduplicate,
    enforce_load_rule,
    extract,
    run,
    verify_source,
)

# A valid source row, by source column.
VALID_ROW: dict[str, str] = {
    "Timestamp": "8/27/2014 11:29",
    "Gender": "Female",
    "Country": "United States",
    "Occupation": "Corporate",
    "self_employed": "",
    "family_history": "No",
    "treatment": "Yes",
    "Days_Indoors": "1-14 days",
    "Growing_Stress": "Yes",
    "Changes_Habits": "No",
    "Mental_Health_History": "Yes",
    "Mood_Swings": "Medium",
    "Coping_Struggles": "No",
    "Work_Interest": "No",
    "Social_Weakness": "Yes",
    "mental_health_interview": "No",
    "care_options": "Not sure",
}


def row(**overrides: str) -> dict[str, str]:
    return VALID_ROW | overrides


def write_source(path: Path, rows: list[dict[str, str]]) -> Path:
    pd.DataFrame(rows, columns=list(SOURCE_COLUMNS)).to_csv(path, index=False)
    return path


def extracted(tmp_path: Path, rows: list[dict[str, str]]) -> pd.DataFrame:
    return extract(write_source(tmp_path / "source.csv", rows))


@pytest.fixture
def connection() -> Iterator[duckdb.DuckDBPyConnection]:
    with duckdb.connect() as connection:
        yield connection


@pytest.fixture
def trust_any_source(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make `run` accept whatever source file a test writes."""
    monkeypatch.setattr(staging, "verify_source", lambda path: None)


def test_a_source_file_with_a_different_sha256_is_rejected(tmp_path: Path) -> None:
    source = write_source(tmp_path / "source.csv", [row()])
    with pytest.raises(SourceChecksumError, match="unaudited"):
        verify_source(source)


def test_a_source_file_with_an_unexpected_header_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    source.write_text("Timestamp,Gender\n8/27/2014 11:29,Female\n")
    with pytest.raises(SourceHeaderError):
        extract(source)


def test_extraction_keeps_empty_fields_as_empty_strings(tmp_path: Path) -> None:
    frame = extracted(tmp_path, [row(self_employed="")])
    assert frame.loc[0, "self_employed"] == ""


def test_extraction_numbers_source_rows_from_one(tmp_path: Path) -> None:
    frame = extracted(tmp_path, [row(), row(), row()])
    assert list(frame[staging.SOURCE_ROW]) == [1, 2, 3]


def test_cleaning_trims_modeled_columns(tmp_path: Path) -> None:
    frame = clean(
        extracted(tmp_path, [row(Gender="  Female ", Timestamp=" 8/27/2014 11:29")])
    )
    assert frame.loc[0, "Gender"] == "Female"
    assert frame.loc[0, "Timestamp"] == "8/27/2014 11:29"


def test_cleaning_rewrites_a_case_variant_to_the_domain_literal(tmp_path: Path) -> None:
    frame = clean(
        extracted(tmp_path, [row(Gender="female", Days_Indoors="GO OUT EVERY DAY")])
    )
    assert frame.loc[0, "Gender"] == "Female"
    assert frame.loc[0, "Days_Indoors"] == "Go out Every day"


def test_cleaning_leaves_a_value_with_no_case_insensitive_match_unchanged(
    tmp_path: Path,
) -> None:
    frame = clean(extracted(tmp_path, [row(Gender="femal")]))
    assert frame.loc[0, "Gender"] == "femal"


def test_cleaning_leaves_unmodeled_columns_unchanged(tmp_path: Path) -> None:
    frame = clean(extracted(tmp_path, [row(Work_Interest=" maybe ")]))
    assert frame.loc[0, "Work_Interest"] == " maybe "


def test_a_value_outside_its_domain_aborts_naming_the_source_row(
    tmp_path: Path,
) -> None:
    frame = clean(extracted(tmp_path, [row(), row(Country="Atlantis")]))
    with pytest.raises(LoadRuleError, match="source row 2, Country: 'Atlantis'"):
        enforce_load_rule(frame)


@pytest.mark.parametrize("value", ["", "   "])
def test_an_empty_modeled_value_aborts(tmp_path: Path, value: str) -> None:
    frame = clean(extracted(tmp_path, [row(Mood_Swings=value)]))
    with pytest.raises(LoadRuleError, match="Mood_Swings"):
        enforce_load_rule(frame)


@pytest.mark.parametrize("value", ["2014-08-27 11:29", "13/27/2014 11:29", ""])
def test_an_unparsable_timestamp_aborts(tmp_path: Path, value: str) -> None:
    frame = clean(extracted(tmp_path, [row(Timestamp=value)]))
    with pytest.raises(LoadRuleError, match="Timestamp"):
        enforce_load_rule(frame)


def test_an_empty_unmodeled_value_does_not_abort(tmp_path: Path) -> None:
    enforce_load_rule(clean(extracted(tmp_path, [row(Changes_Habits="")])))


def test_the_violation_message_counts_every_violation(tmp_path: Path) -> None:
    frame = clean(extracted(tmp_path, [row(Gender="X")] * 12))
    with pytest.raises(LoadRuleError, match="^12 load-rule violation"):
        enforce_load_rule(frame)


def test_deduplication_keeps_the_first_occurrence(tmp_path: Path) -> None:
    frame = deduplicate(clean(extracted(tmp_path, [row(), row(Gender="Male"), row()])))
    assert list(frame[staging.SOURCE_ROW]) == [1, 2]


def test_rows_differing_only_in_an_unmodeled_column_are_not_duplicates(
    tmp_path: Path,
) -> None:
    frame = deduplicate(
        clean(extracted(tmp_path, [row(Work_Interest="No"), row(Work_Interest="Yes")]))
    )
    assert len(frame) == 2


def test_deduplication_discards_the_unmodeled_columns(tmp_path: Path) -> None:
    frame = deduplicate(clean(extracted(tmp_path, [row()])))
    assert list(frame.columns) == [
        staging.SOURCE_ROW,
        *staging.STAGING_COLUMNS.values(),
    ]


@pytest.mark.usefixtures("trust_any_source")
def test_a_run_loads_one_row_per_staged_record_with_ids_in_source_order(
    tmp_path: Path, connection: duckdb.DuckDBPyConnection
) -> None:
    source = write_source(
        tmp_path / "source.csv", [row(), row(Gender="Male"), row(), row(Gender="Male")]
    )
    report = run(connection, source)
    staged = connection.execute(
        "SELECT response_id, gender FROM staging_response ORDER BY response_id"
    ).fetchall()
    assert report == staging.StagingReport(
        raw_rows=4, duplicates_removed=2, staged_rows=2
    )
    assert staged == [(1, "Female"), (2, "Male")]


@pytest.mark.usefixtures("trust_any_source")
def test_a_second_run_replaces_the_first_instead_of_appending(
    tmp_path: Path, connection: duckdb.DuckDBPyConnection
) -> None:
    source = write_source(tmp_path / "source.csv", [row(), row(Gender="Male")])
    run(connection, source)
    run(connection, source)
    count = connection.execute("SELECT COUNT(*) FROM staging_response").fetchone()
    assert count == (2,)


@pytest.mark.usefixtures("trust_any_source")
def test_an_aborted_run_leaves_staging_unchanged(
    tmp_path: Path, connection: duckdb.DuckDBPyConnection
) -> None:
    run(connection, write_source(tmp_path / "good.csv", [row()]))
    with pytest.raises(LoadRuleError):
        run(connection, write_source(tmp_path / "bad.csv", [row(Gender="X")]))
    count = connection.execute("SELECT COUNT(*) FROM staging_response").fetchone()
    assert count == (1,)


def test_a_failed_insert_rolls_staging_back(
    tmp_path: Path, connection: duckdb.DuckDBPyConnection
) -> None:
    create_schema(connection)
    good = deduplicate(clean(extracted(tmp_path, [row()])))
    staging.load_staging(connection, good)
    broken = good.assign(response_timestamp="not a timestamp")
    with pytest.raises(duckdb.Error) as raised:
        staging.load_staging(connection, broken)
    count = connection.execute("SELECT COUNT(*) FROM staging_response").fetchone()
    assert count == (1,)
    assert "while loading staging_response" in raised.value.__notes__
