"""Exposure of the indicator output: two runs, their hashes, and the value scan.

Implements ADR-0011, rule 5, and the first item of its Confirmation. The
sixteen indicators are computed on two full reloads, each into its own
database file, and serialized in one canonical form:

* UTF-8 CSV with a header row; columns in query order; rows in the query's
  `ORDER BY`; RFC 4180 quoting only where required; LF line endings and a
  trailing newline;
* NULL as an empty field; booleans as `true` and `false`; integers without
  decimals; rates rounded once, here, at `DECIMALS` places, half away from
  zero, on the exact binary value of the computed rate.

The output of the first run is written to `EVIDENCE_DIR`, one file per
indicator; `hashes.csv` holds the SHA-256 of each indicator under both runs and
whether the two are identical.

The value scan searches every commit reachable from `SCAN_TIP`, trees and
messages, for each indicator value in the forms that `search_terms` lists, and
writes one row per value and path at the first commit that holds it, with the
class that commit falls in. The columns `nature` and `note` are filled by
reading each hit; a rerun keeps them for rows it finds again.

Run from the repository root: `uv run python -m stress_dw.evidence`.
"""

import csv
import hashlib
import io
import re
import subprocess
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from functools import cache
from pathlib import Path

import duckdb
import pandas as pd

from stress_dw.indicators import INDICATORS, run_indicator
from stress_dw.pipeline import SOURCE_PATH, run_pipeline

EVIDENCE_DIR = Path("docs/audit/correspondence-evidence")
RUN_DATABASES = (
    Path("data/evidence-run-1.duckdb"),
    Path("data/evidence-run-2.duckdb"),
)
HASHES_FILE = "hashes.csv"
SCAN_FILE = "value-scan.csv"

# Decimal places of a serialized rate.
DECIMALS = 6
RATE_COLUMNS = frozenset({"rate", "headline_rate"})
COUNT_COLUMNS = frozenset({"numerator", "denominator"})

# The criteria commit (#75), the commit that recorded A5, A6 and A10 (#79),
# after which exposure is allowed (ADR-0011, rule 4), and the last commit of
# `main` before the scan.
CRITERIA_COMMIT = "ed49662"
EXPOSURE_COMMIT = "b278bec"
SCAN_TIP = "8b67c52"

# Counts below this floor occur everywhere as unrelated numbers, so a hit
# could not be told from noise; they are not searched.
COUNT_FLOOR = 1000
FRACTION_DECIMALS = (6, 4, 3)
PERCENT_DECIMALS = (1, 2)

BEFORE_CRITERIA = "failure of (i)"
POST_COMMIT = "post-commit exposure"
IN_ORDER = "in order"
MESSAGE_PATH = "(commit message)"
SCAN_HEADER = ("value", "indicator", "commit", "path", "class", "nature", "note")

# A number as written in prose, code or a CSV field: digits with optional
# commas and an optional decimal part, not inside a word, an identifier, a
# hash or a longer number, and optionally followed by a percent sign.
NUMBER = re.compile(r"(?<![\w.,])(\d[\d,]*(?:\.\d+)?)(?!\w)(?!\.\d)( ?%)?")
GROUPED = re.compile(r"\d{1,3}(?:,\d{3})+")


def rounded(value: Decimal | float, decimals: int) -> str:
    """Round `value` half away from zero at `decimals` places, as text."""
    exponent = Decimal(1).scaleb(-decimals)
    return str(Decimal(value).quantize(exponent, rounding=ROUND_HALF_UP))


def serialize_cell(column: str, value: object) -> str:
    """Serialize one cell of an indicator's output in the canonical form.

    Raises:
        TypeError: a float outside `RATE_COLUMNS`, or a type the indicator
            queries do not produce.
    """
    if value is None or value is pd.NA or (isinstance(value, float) and value != value):
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if column not in RATE_COLUMNS:
            raise TypeError(f"column {column}: a float outside the rate columns")
        return rounded(value, DECIMALS)
    if isinstance(value, str):
        return value
    raise TypeError(f"column {column}: unexpected type {type(value).__name__}")


def serialize(frame: pd.DataFrame) -> bytes:
    """Serialize an indicator's output, columns and rows in the given order."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    columns = [str(c) for c in frame.columns]
    writer.writerow(columns)
    for row in frame.astype(object).itertuples(index=False, name=None):
        writer.writerow(
            serialize_cell(c, v.item() if hasattr(v, "item") else v)
            for c, v in zip(columns, row, strict=True)
        )
    return buffer.getvalue().encode("utf-8")


def run_once(database: Path) -> dict[int, bytes]:
    """Reload `database` from scratch and serialize the sixteen indicators."""
    for stale in (database, database.with_name(database.name + ".wal")):
        stale.unlink(missing_ok=True)
    with duckdb.connect(database) as connection:
        run_pipeline(connection, SOURCE_PATH)
        return {n: serialize(run_indicator(connection, n).rows) for n in INDICATORS}


def sha256(data: bytes) -> str:
    """Return the hex SHA-256 of `data`."""
    return hashlib.sha256(data).hexdigest()


def indicator_file(number: int) -> str:
    """Return the file name of indicator `number`'s output."""
    return f"indicator-{number:02d}.csv"


def search_terms(outputs: Mapping[int, bytes]) -> dict[tuple[str, bool], set[int]]:
    """List the written forms of each indicator value, and their indicators.

    A key is a form and whether it must be followed by a percent sign. Counts
    (`COUNT_COLUMNS`) of `COUNT_FLOOR` or more: plain and with thousands
    commas. Rates: as fractions at `FRACTION_DECIMALS` places, as percentages at
    `PERCENT_DECIMALS` places, and as whole percentages, the last only with
    the percent sign.
    """
    terms: dict[tuple[str, bool], set[int]] = {}
    for number, data in outputs.items():
        for row in csv.DictReader(io.StringIO(data.decode("utf-8"))):
            for column, text in row.items():
                forms: list[tuple[str, bool]] = []
                if column in RATE_COLUMNS and text:
                    rate = Decimal(text)
                    forms += [(rounded(rate, d), False) for d in FRACTION_DECIMALS]
                    forms += [(rounded(rate * 100, d), False) for d in PERCENT_DECIMALS]
                    forms.append((rounded(rate * 100, 0), True))
                elif column in COUNT_COLUMNS and int(text) >= COUNT_FLOOR:
                    forms += [(text, False), (f"{int(text):,}", False)]
                for form in forms:
                    terms.setdefault(form, set()).add(number)
    return terms


def numbers_in(text: str) -> Iterator[tuple[str, bool]]:
    """Yield each number written in `text`, and whether a percent sign follows.

    A run of digits and commas that is not a number with thousands commas,
    such as a CSV row, is split at the commas.
    """
    for match in NUMBER.finditer(text):
        body = match.group(1).rstrip(",")
        percent = match.group(2) is not None
        if "," not in body or GROUPED.fullmatch(body):
            yield body, percent
            continue
        parts = body.split(",")
        for index, part in enumerate(parts):
            if part:
                yield part, percent and index == len(parts) - 1


def matches(
    text: str, terms: Mapping[tuple[str, bool], set[int]]
) -> Iterator[tuple[str, set[int]]]:
    """Yield each form of `terms` written in `text`, with its indicators."""
    for body, percent in numbers_in(text):
        found = terms.get((body, False), set())
        if percent:
            found = found | terms.get((body, True), set())
        if found:
            yield body + ("%" if percent and (body, True) in terms else ""), found


def git(*arguments: str) -> bytes:
    """Run a read-only git command in the repository and return its output."""
    return subprocess.run(["git", *arguments], check=True, capture_output=True).stdout


def is_ancestor(commit: str, of: str) -> bool:
    """Return whether `commit` is `of` or one of its ancestors."""
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, of], check=False
    )
    return result.returncode == 0


def changed_blobs(commit: str, parents: list[str]) -> Iterator[tuple[str, str]]:
    """Yield (path, blob) for each file `commit` adds or changes.

    Against its first parent; for the root commit, every file of its tree.
    """
    if parents:
        raw = git("diff-tree", "-r", "-z", "--no-commit-id", parents[0], commit)
        fields = raw.decode("utf-8").split("\0")
        for header, path in zip(fields[0::2], fields[1::2], strict=False):
            _, _, _, blob, status = header.split(" ")
            if not status.startswith("D"):
                yield path, blob
        return
    raw = git("ls-tree", "-r", "-z", commit)
    for entry in raw.decode("utf-8").split("\0"):
        if entry:
            header, path = entry.split("\t", 1)
            yield path, header.split(" ")[2]


@cache
def commit_class(commit: str) -> str:
    """Classify a commit against the criteria commit and the exposure commit."""
    if is_ancestor(commit, CRITERIA_COMMIT):
        return BEFORE_CRITERIA
    if is_ancestor(commit, EXPOSURE_COMMIT) and not is_ancestor(
        EXPOSURE_COMMIT, commit
    ):
        return POST_COMMIT
    return IN_ORDER


@dataclass(frozen=True)
class Hit:
    """The first commit at which a value is written at a path."""

    value: str
    indicators: tuple[int, ...]
    commit: str
    path: str
    commit_class: str


def scan(terms: Mapping[tuple[str, bool], set[int]]) -> list[Hit]:
    """Find each value of `terms` in the history up to `SCAN_TIP`."""
    hits: dict[tuple[str, str], Hit] = {}
    listing = git("rev-list", "--topo-order", "--reverse", "--parents", SCAN_TIP)
    for line in listing.decode("utf-8").splitlines():
        commit, *parents = line.split()
        texts: list[tuple[str, str]] = [
            (MESSAGE_PATH, git("log", "-1", "--format=%B", commit).decode("utf-8"))
        ]
        for path, blob in changed_blobs(commit, parents):
            data = git("cat-file", "blob", blob)
            if b"\0" not in data:
                texts.append((path, data.decode("utf-8", errors="replace")))
        for path, text in texts:
            for value, indicators in matches(text, terms):
                if (value, path) not in hits:
                    hits[value, path] = Hit(
                        value,
                        tuple(sorted(indicators)),
                        commit[:7],
                        path,
                        commit_class(commit),
                    )
    return list(hits.values())


def read_annotations(path: Path) -> dict[tuple[str, str, str], tuple[str, str]]:
    """Read `nature` and `note` of an earlier scan, keyed by value, commit, path."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as handle:
        return {
            (row["value"], row["commit"], row["path"]): (row["nature"], row["note"])
            for row in csv.DictReader(handle)
        }


def write_rows(
    path: Path, header: Iterable[str], rows: Iterable[Iterable[object]]
) -> None:
    """Write a UTF-8 CSV with a header row and LF line endings."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def main() -> None:
    """Run both reloads, write the outputs and hashes, then scan the history."""
    first, second = (run_once(database) for database in RUN_DATABASES)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    for number, data in first.items():
        (EVIDENCE_DIR / indicator_file(number)).write_bytes(data)
    comparison = [
        (n, sha256(first[n]), sha256(second[n]), first[n] == second[n])
        for n in INDICATORS
    ]
    write_rows(
        EVIDENCE_DIR / HASHES_FILE,
        ("indicator", "sha256_run_1", "sha256_run_2", "identical"),
        ((n, a, b, "true" if same else "false") for n, a, b, same in comparison),
    )
    identical = sum(same for *_, same in comparison)
    print(f"indicators identical across the two runs: {identical} of {len(comparison)}")

    scan_path = EVIDENCE_DIR / SCAN_FILE
    annotations = read_annotations(scan_path)
    hits = sorted(scan(search_terms(first)), key=lambda h: (h.path, h.value))
    write_rows(
        scan_path,
        SCAN_HEADER,
        (
            (
                h.value,
                ";".join(str(i) for i in h.indicators),
                h.commit,
                h.path,
                h.commit_class,
                *annotations.get((h.value, h.commit, h.path), ("", "")),
            )
            for h in hits
        ),
    )
    by_class = {
        c: sum(h.commit_class == c for h in hits)
        for c in (BEFORE_CRITERIA, POST_COMMIT, IN_ORDER)
    }
    print(f"scan hits: {len(hits)}; by class: {by_class}")


if __name__ == "__main__":
    main()
