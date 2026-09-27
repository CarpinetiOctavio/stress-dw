from pathlib import Path

import duckdb
import pandas as pd
import pytest

from stress_dw import staging
from stress_dw.pipeline import run_pipeline
from stress_dw.staging import SOURCE_COLUMNS

ROW: dict[str, str] = {
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


def test_a_run_loads_staging_every_dimension_and_one_fact_row_per_staged_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(staging, "verify_source", lambda path: None)
    source = tmp_path / "source.csv"
    rows = [ROW, ROW | {"Gender": "Male"}, ROW, ROW | {"Country": "Brazil"}]
    pd.DataFrame(rows, columns=list(SOURCE_COLUMNS)).to_csv(source, index=False)
    with duckdb.connect() as connection:
        report = run_pipeline(connection, source)
        orphans = connection.execute(
            """
            SELECT COUNT(*) FROM fact_response
            LEFT JOIN dim_gender USING (gender_id)
            WHERE dim_gender.gender IS NULL
            """
        ).fetchone()
    assert report.staging.raw_rows == 4
    assert report.staging.staged_rows == 3
    assert report.warehouse.fact_rows == 3
    assert report.warehouse.dimension_rows["dim_gender"] == 2
    assert report.warehouse.dimension_rows["dim_country"] == 2
    assert orphans == (0,)
