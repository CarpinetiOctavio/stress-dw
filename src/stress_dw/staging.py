"""Populate `staging_response` from the source file (docs/specification/staging.md).

Steps run in the order staging.md fixes: verify the source file, extract,
clean, enforce the load rule, deduplicate, load. Running this module performs
a full reload into the project's DuckDB file and prints the load report:

    uv run python -m stress_dw.staging
"""

import hashlib
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

import duckdb
import pandas as pd

from stress_dw.domains import DOMAINS, TIMESTAMP_FORMAT
from stress_dw.schema import ensure_schema

SOURCE_PATH = Path("data/raw/mental_health.csv")
DATABASE_PATH = Path("data/stress_dw.duckdb")
SOURCE_SHA256 = "083f44e9cdf84f56abf08b9fa1862d80b87237afa74e2cacc9328a63d9291686"

# The 17 source columns, in file order (docs/specification/sources.md#column-map).
SOURCE_COLUMNS: tuple[str, ...] = (
    "Timestamp",
    "Gender",
    "Country",
    "Occupation",
    "self_employed",
    "family_history",
    "treatment",
    "Days_Indoors",
    "Growing_Stress",
    "Changes_Habits",
    "Mental_Health_History",
    "Mood_Swings",
    "Coping_Struggles",
    "Work_Interest",
    "Social_Weakness",
    "mental_health_interview",
    "care_options",
)

# The 13 modeled source columns, mapped to their `staging_response` column.
STAGING_COLUMNS: dict[str, str] = {
    "Timestamp": "response_timestamp",
    "Gender": "gender",
    "Country": "country",
    "Occupation": "occupation",
    "family_history": "family_history",
    "treatment": "treatment",
    "Days_Indoors": "days_indoors",
    "Growing_Stress": "growing_stress",
    "Mood_Swings": "mood_swings",
    "Coping_Struggles": "coping_struggles",
    "Social_Weakness": "social_weakness",
    "mental_health_interview": "mental_health_interview",
    "care_options": "care_options",
}

# Column added at extraction: the row's 1-based position among the source
# file's data rows, header excluded. Identifies a row in error messages.
SOURCE_ROW = "source_row"

# How many violations a LoadRuleError message lists before summarizing.
MAX_REPORTED_VIOLATIONS = 10


class SourceChecksumError(ValueError):
    """The source file's SHA-256 is not the audited file's."""


class SourceHeaderError(ValueError):
    """The source file's header is not the 17 expected columns, in order."""


class LoadRuleError(ValueError):
    """A modeled column holds a NULL or a value outside its documented domain."""


@dataclass(frozen=True)
class StagingReport:
    """The three counts ADR-0008's Confirmation requires of a staging load."""

    raw_rows: int
    duplicates_removed: int
    staged_rows: int


def verify_source(path: Path) -> None:
    """Abort unless `path` is byte-identical to the audited source file.

    Raises:
        SourceChecksumError: The file's SHA-256 differs from `SOURCE_SHA256`.
    """
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != SOURCE_SHA256:
        raise SourceChecksumError(
            f"{path}: SHA-256 {digest} does not match the audited source file's "
            f"{SOURCE_SHA256}; refusing to load an unaudited dataset"
        )


def extract(path: Path) -> pd.DataFrame:
    """Read all 17 source columns as text, plus `SOURCE_ROW`.

    Every cell is read as its literal text: an empty field is the empty
    string, never NaN, so no value is interpreted before cleaning.

    Raises:
        SourceHeaderError: The header is not `SOURCE_COLUMNS`, in order.
    """
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    if tuple(frame.columns) != SOURCE_COLUMNS:
        raise SourceHeaderError(
            f"{path}: header {list(frame.columns)} is not {list(SOURCE_COLUMNS)}"
        )
    frame[SOURCE_ROW] = range(1, len(frame) + 1)
    return frame


def clean(frame: pd.DataFrame) -> pd.DataFrame:
    """Trim and case-normalize the modeled columns of an extracted frame.

    Implements docs/specification/staging.md#cleaning-and-normalization: the
    thirteen modeled columns are trimmed; each of the twelve with an
    enumerated domain has a value that matches a domain literal
    case-insensitively rewritten to that literal. Any other value, and every
    unmodeled column, is left unchanged.
    """
    cleaned = frame.copy()
    for column in STAGING_COLUMNS:
        cleaned[column] = cleaned[column].str.strip()
    for column, domain in DOMAINS.items():
        by_lowercase = {literal.lower(): literal for literal in domain}
        normalized = cleaned[column].str.lower().map(by_lowercase)
        cleaned[column] = normalized.fillna(cleaned[column])
    return cleaned


def enforce_load_rule(frame: pd.DataFrame) -> None:
    """Abort if any modeled column of a cleaned frame breaks the load rule.

    Implements docs/specification/sources.md#load-rule: an empty value, a
    value outside its column's domain, or a `Timestamp` that does not parse
    as `TIMESTAMP_FORMAT` aborts the load. Nothing is dropped or recoded.

    Raises:
        LoadRuleError: Lists the source row, column, and value of each
            violation, up to `MAX_REPORTED_VIOLATIONS`, and the total count.
    """
    violations: list[str] = []
    for column in STAGING_COLUMNS:
        values = frame[column]
        if column in DOMAINS:
            invalid = ~values.isin(DOMAINS[column])
        else:
            parsed = pd.to_datetime(values, format=TIMESTAMP_FORMAT, errors="coerce")
            invalid = parsed.isna()
        for source_row, value in zip(
            frame.loc[invalid, SOURCE_ROW], values[invalid], strict=True
        ):
            violations.append(f"source row {source_row}, {column}: {value!r}")
    if violations:
        listed = "; ".join(violations[:MAX_REPORTED_VIOLATIONS])
        raise LoadRuleError(
            f"{len(violations)} load-rule violation(s), load aborted: {listed}"
        )


def deduplicate(frame: pd.DataFrame) -> pd.DataFrame:
    """Keep the first occurrence of each row, compared on all 17 source columns.

    Implements ADR-0008. Returns the surviving rows in source-file order, with
    the four unmodeled columns discarded and the modeled ones renamed to their
    `staging_response` names; `SOURCE_ROW` is kept.
    """
    kept = frame[~frame.duplicated(subset=list(SOURCE_COLUMNS), keep="first")]
    return kept[[SOURCE_ROW, *STAGING_COLUMNS]].rename(columns=STAGING_COLUMNS)


def load_staging(connection: duckdb.DuckDBPyConnection, frame: pd.DataFrame) -> None:
    """Replace the contents of `staging_response` with a deduplicated frame.

    Assigns `response_id` 1..N in the frame's order, which `deduplicate`
    leaves in source-file order. One transaction: on failure,
    `staging_response` keeps whatever it held before.
    """
    staged_frame = frame.drop(columns=SOURCE_ROW)
    staged_frame.insert(0, "response_id", range(1, len(staged_frame) + 1))
    insert = (
        files("stress_dw") / "sql" / "staging" / "insert_staging_response.sql"
    ).read_text()
    connection.register("staged_frame", staged_frame)
    connection.begin()
    try:
        connection.execute("DELETE FROM staging_response")
        connection.execute(insert, [TIMESTAMP_FORMAT])
    except duckdb.Error as error:
        connection.rollback()
        error.add_note("while loading staging_response")
        raise
    else:
        connection.commit()
    finally:
        connection.unregister("staged_frame")


def run(connection: duckdb.DuckDBPyConnection, path: Path) -> StagingReport:
    """Run every staging step against `path` and load the result.

    Creates any missing table first, so a new database file needs no setup.
    """
    verify_source(path)
    extracted = extract(path)
    cleaned = clean(extracted)
    enforce_load_rule(cleaned)
    deduplicated = deduplicate(cleaned)
    ensure_schema(connection)
    load_staging(connection, deduplicated)
    return StagingReport(
        raw_rows=len(extracted),
        duplicates_removed=len(extracted) - len(deduplicated),
        staged_rows=len(deduplicated),
    )


def main() -> None:
    """Fully reload `staging_response` in `DATABASE_PATH` and print the report."""
    with duckdb.connect(DATABASE_PATH) as connection:
        report = run(connection, SOURCE_PATH)
    print(f"raw rows:           {report.raw_rows:>9,}")
    print(f"duplicates removed: {report.duplicates_removed:>9,}")
    print(f"staged rows:        {report.staged_rows:>9,}")


if __name__ == "__main__":
    main()
