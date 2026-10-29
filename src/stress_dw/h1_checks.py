"""Checks A5, A6 and A10 of docs/audit/legacy-audit.md, and the branch they set.

Implements docs/audit/correspondence-criteria.md, section 3.4, with its
amendment of 2026-10-29 (section 7): the two units, the harmonization of
values (LOG-050, item 2; section 3.5), the measures, their interpretability
bound and their outcomes, and the mapping rule R0 to R5.

No contingency table, and no count or share of a column of the source file,
is returned for output: a marginal of the records unit can equal an
indicator's numerators (ADR-0011, rule 1). The values of V, w and w_d, and
A10's marginal comparisons, are written only with `--with-values`, once
exposure is allowed (section 7, amendment of 2026-10-29).

Run: `uv run python -m stress_dw.h1_checks`, with the two external copies at
`OSMI_PATH` and `RHMCD_PATH`; each is verified by its SHA-256 before it is read.
"""

import argparse
import csv
import hashlib
import math
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import StrEnum
from itertools import combinations
from pathlib import Path

import pandas as pd

from stress_dw.domains import DOMAINS, TIMESTAMP_FORMAT
from stress_dw.pipeline import SOURCE_PATH
from stress_dw.staging import (
    SOURCE_COLUMNS,
    clean,
    enforce_load_rule,
    extract,
    verify_source,
)

# The two column groups of H1, per LOG-040.
OSMI_GROUP: tuple[str, ...] = (
    "Timestamp",
    "Gender",
    "Country",
    "self_employed",
    "family_history",
    "treatment",
    "mental_health_interview",
    "care_options",
)
SYMPTOM_COLUMNS: tuple[str, ...] = (
    "Days_Indoors",
    "Growing_Stress",
    "Changes_Habits",
    "Mental_Health_History",
    "Mood_Swings",
    "Coping_Struggles",
    "Work_Interest",
    "Social_Weakness",
)
OCCUPATION = "Occupation"
CARE_OPTIONS = "care_options"
TIMESTAMP = "Timestamp"

# The four source columns with no documented domain and no staging column.
UNMODELED_COLUMNS: tuple[str, ...] = (
    "self_employed",
    "Changes_Habits",
    "Mental_Health_History",
    "Work_Interest",
)

# Columns of the profile unit: the 16 other than `Timestamp` (ADR-0001, H2).
PROFILE_COLUMNS: tuple[str, ...] = tuple(c for c in SOURCE_COLUMNS if c != TIMESTAMP)

# Small effect for w (Cohen 1988, pp. 224-225), and the interpretability bound,
# half of it (LOG-050, item 1).
SMALL = 0.10
INTERPRETABILITY_BOUND = SMALL / 2
# Significance criterion of A10's guard (LOG-050, item 3).
ALPHA = 0.05

# A null is a category of its own in A5 and A6 (LOG-050, item 2).
NULL = "<null>"
# Category of A6's identity list for an external value that matches no label.
UNMATCHED = "<unmatched>"

# The external copies, by fixed path and SHA-256, as recorded in rows A6 and
# A10 of docs/audit/legacy-audit.md; outputs go to `CHECKS_DIR`.
OSMI_PATH = Path("data/external/osmi-2014/openml-43664.arff")
OSMI_SHA256 = "abd6cad25bcfa4293d7bbdb038eec0c64d54305878aad0ed24e0e377cc07b45d"
RHMCD_PATH = Path("data/external/rhmcd-20/mental_health_finaldata_1.csv")
RHMCD_SHA256 = "bb6be8f14e8a6718f9974942b3120e75b3959a3f425b1b2309ebd67d0d5c39a0"
CHECKS_DIR = Path("docs/audit/checks")

# Branches of the mapping rule (section 3.4).
H1_HOLDS = "H1 holds"
H1_DOES_NOT_HOLD = "H1 does not hold"
BOTH_BRANCHES = "both, without resolving"

# Format of OSMI 2014's `Timestamp`, and the year-and-month grain of both.
OSMI_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
YEAR_MONTH_FORMAT = "%Y-%m"


class Unit(StrEnum):
    """The two units of section 3.4, Units, and A10's set F."""

    RECORDS = "records"
    PROFILES = "profiles"
    SET_F = "set_f"


class ExternalDataError(ValueError):
    """An external copy is not the recorded file, or lacks a compared column."""


@dataclass(frozen=True)
class PairResult:
    """A5 on one pair of columns, in one unit."""

    unit: Unit
    column_1: str
    column_2: str
    pair_class: str
    rows: int
    columns: int
    n: int
    cramers_v: float
    w: float
    noise_floor: float

    @property
    def interpretable(self) -> bool:
        """Whether the noise floor is below the interpretability bound."""
        return self.noise_floor < INTERPRETABILITY_BOUND

    @property
    def at_or_above_small(self) -> bool:
        """Whether w is at or above Small (section 3.4, Operative criterion)."""
        return self.w >= SMALL


@dataclass(frozen=True)
class ColumnResult:
    """A6 on one column, in one unit."""

    unit: Unit
    column: str
    categories: int
    n_file: int
    n_osmi: int
    w_d: float
    noise_floor: float

    @property
    def interpretable(self) -> bool:
        """Whether the noise floor is below the interpretability bound."""
        return self.noise_floor < INTERPRETABILITY_BOUND

    @property
    def result(self) -> str:
        """Concordant, discordant or indeterminate (section 3.4, A6)."""
        if not self.interpretable:
            return "indeterminate"
        return "discordant" if self.w_d >= SMALL else "concordant"


@dataclass(frozen=True)
class Guard:
    """A10's chance model under one set of marginals (amendment of 2026-10-29)."""

    marginals: Unit
    q: float
    log10_g: float

    @property
    def below_alpha(self) -> bool:
        """Whether G < α, compared on logarithms so that G cannot underflow."""
        return self.log10_g < math.log10(ALPHA)


@dataclass(frozen=True)
class ContainmentResult:
    """A10's containment test of F in R, and its outcome."""

    f_size: int
    f_null_excluded: int
    r_size: int
    r_null_excluded: int
    c: float
    c_1: float
    records_exact: float
    records_near: float
    guards: tuple[Guard, ...]

    @property
    def outcome(self) -> str:
        """Confirms only if c = 1 and G < α under all three sets of marginals."""
        if self.c == 1 and all(guard.below_alpha for guard in self.guards):
            return "confirms"
        return "does not confirm"


def sha256_of(path: Path) -> str:
    """Return the SHA-256 of a file's bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_external(path: Path, expected: str) -> None:
    """Abort unless `path` is byte-identical to the recorded external copy.

    Raises:
        ExternalDataError: The file's SHA-256 differs from `expected`.
    """
    digest = sha256_of(path)
    if digest != expected:
        raise ExternalDataError(
            f"{path}: SHA-256 {digest} does not match the recorded copy's {expected}"
        )


def harmonize_unmodeled(frame: pd.DataFrame) -> pd.DataFrame:
    """Trim the four unmodeled columns and merge values that differ only in case.

    Implements LOG-050, item 2: each group of values equal after case-folding
    is merged under its most frequent form; a tie goes to the form that sorts
    first by Unicode code point (criteria document, section 3.4, Units). An
    empty value becomes `NULL`.
    """
    harmonized = frame.copy()
    for column in UNMODELED_COLUMNS:
        values = harmonized[column].str.strip()
        counts = Counter(values)
        forms: dict[str, list[str]] = {}
        for value in counts:
            forms.setdefault(value.casefold(), []).append(value)
        chosen = {
            folded: min(group, key=lambda form: (-counts[form], form))
            for folded, group in forms.items()
        }
        merged = values.map({value: chosen[value.casefold()] for value in counts})
        harmonized[column] = merged.mask(merged == "", NULL)
    return harmonized


def records_unit(path: Path) -> pd.DataFrame:
    """Return the records unit: staging's rows, with all 17 columns harmonized.

    Runs staging's verification, extraction, cleaning and load rule, then
    removes exact duplicates on the 17 source columns (ADR-0008) without
    discarding the four unmodeled columns. `Timestamp` is reduced to year and
    month, the grain of `dim_time`.
    """
    verify_source(path)
    cleaned = clean(extract(path))
    enforce_load_rule(cleaned)
    kept = cleaned[~cleaned.duplicated(subset=list(SOURCE_COLUMNS), keep="first")]
    unit = harmonize_unmodeled(kept[list(SOURCE_COLUMNS)])
    timestamps = pd.to_datetime(unit[TIMESTAMP], format=TIMESTAMP_FORMAT)
    unit[TIMESTAMP] = timestamps.dt.strftime(YEAR_MONTH_FORMAT)
    return unit.reset_index(drop=True)


def profile_unit(records: pd.DataFrame) -> pd.DataFrame:
    """Return the distinct profiles of the records unit on `PROFILE_COLUMNS`."""
    return records[list(PROFILE_COLUMNS)].drop_duplicates().reset_index(drop=True)


def chi_squared(table: pd.DataFrame) -> float:
    """Return Pearson's χ² of a contingency table of counts."""
    n = table.to_numpy().sum()
    expected = (
        table.sum(axis=1).to_numpy()[:, None] * table.sum(axis=0).to_numpy()[None, :]
    ) / n
    return float((((table.to_numpy() - expected) ** 2) / expected).sum())


def pair_class(column_1: str, column_2: str, care_options_excluded: bool) -> str:
    """Classify a pair for A5's aggregation (section 3.4, A5: outcome)."""
    pair = {column_1, column_2}
    if OCCUPATION in pair:
        return "excluded: Occupation"
    if care_options_excluded and CARE_OPTIONS in pair:
        return "excluded: care_options"
    in_osmi = sum(column in OSMI_GROUP for column in pair)
    if in_osmi == 2:
        return "within-OSMI"
    if in_osmi == 1:
        return "cross"
    return "within other group"


def association(
    frame: pd.DataFrame,
    column_1: str,
    column_2: str,
    unit: Unit,
    care_options_excluded: bool,
) -> PairResult:
    """Compute V, w and the noise floor b of one pair (section 3.4, A5).

    w = √(χ²/n); V = w/√(min(r − 1, c − 1)); b = √((r − 1)(c − 1)/(n − 1)).
    Assumes nulls are already the category `NULL`.
    """
    table = pd.crosstab(frame[column_1], frame[column_2])
    rows, columns = table.shape
    n = int(table.to_numpy().sum())
    smaller = min(rows, columns) - 1
    w = math.sqrt(chi_squared(table) / n) if smaller > 0 else 0.0
    return PairResult(
        unit=unit,
        column_1=column_1,
        column_2=column_2,
        pair_class=pair_class(column_1, column_2, care_options_excluded),
        rows=rows,
        columns=columns,
        n=n,
        cramers_v=w / math.sqrt(smaller) if smaller > 0 else 0.0,
        w=w,
        noise_floor=math.sqrt((rows - 1) * (columns - 1) / (n - 1)),
    )


def a5_pairs(
    records: pd.DataFrame, profiles: pd.DataFrame, care_options_excluded: bool
) -> list[PairResult]:
    """Compute A5 on every pair of both units.

    `Timestamp`'s pairs exist only in the records unit (section 3.4, Units).
    """
    results = [
        association(records, a, b, Unit.RECORDS, care_options_excluded)
        for a, b in combinations(SOURCE_COLUMNS, 2)
    ]
    results += [
        association(profiles, a, b, Unit.PROFILES, care_options_excluded)
        for a, b in combinations(PROFILE_COLUMNS, 2)
    ]
    return results


def a5_outcome(pairs: Iterable[PairResult]) -> str:
    """Return contradicts, supports or indeterminate for the pairs of one unit."""
    pairs = list(pairs)
    cross = [p for p in pairs if p.pair_class == "cross"]
    within = [p for p in pairs if p.pair_class == "within-OSMI"]
    if any(p.interpretable and p.at_or_above_small for p in cross):
        return "contradicts"
    if all(p.interpretable and not p.at_or_above_small for p in cross) and any(
        p.interpretable and p.at_or_above_small for p in within
    ):
        return "supports"
    return "indeterminate"


def outcome_by_unit(pairs: Sequence[PairResult]) -> dict[str, str]:
    """Return A5's outcome per unit and over both (section 3.4, Units).

    `Timestamp`'s pairs, evaluated once on the records unit, enter both.
    """
    timestamp_pairs = [p for p in pairs if TIMESTAMP in (p.column_1, p.column_2)]
    records = a5_outcome(p for p in pairs if p.unit is Unit.RECORDS)
    profiles = a5_outcome(
        [p for p in pairs if p.unit is Unit.PROFILES] + timestamp_pairs
    )
    combined = records if records == profiles else "indeterminate"
    return {"records": records, "profiles": profiles, "combined": combined}


def read_osmi(path: Path) -> pd.DataFrame:
    """Read the OSMI 2014 ARFF file into text columns; `?` becomes `NULL`.

    Raises:
        ExternalDataError: A column of the OSMI group is missing.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    names = [line.split()[1] for line in lines if line.lower().startswith("@attribute")]
    start = next(i for i, line in enumerate(lines) if line.lower() == "@data") + 1
    reader = csv.reader(
        lines[start:], quotechar="'", escapechar="\\", skipinitialspace=True
    )
    rows = [row for row in reader if row]
    frame = pd.DataFrame(rows, columns=names, dtype=str)
    missing = [column for column in OSMI_GROUP if column not in frame.columns]
    if missing:
        raise ExternalDataError(f"{path}: no column {missing}")
    return frame.mask(frame == "?", NULL)


def a6_categories(
    file_values: pd.Series, osmi_values: pd.Series, column: str
) -> tuple[pd.Series, pd.Series]:
    """Harmonize one A6 column on both sides (LOG-050, item 2; section 3.5).

    Both sides are trimmed and case-folded. In a column with a documented
    domain, an OSMI value maps to the label it equals after the same
    normalization, and any other value to `UNMATCHED`. A column with no
    documented domain keeps its normalized values. `NULL` stays `NULL`.
    """

    def normalize(values: pd.Series) -> pd.Series:
        return values.where(values == NULL, values.str.strip().str.casefold())

    file_side, osmi_side = normalize(file_values), normalize(osmi_values)
    if column in DOMAINS:
        labels = {label.casefold() for label in DOMAINS[column]}
        osmi_side = osmi_side.where(
            osmi_side.isin(labels) | (osmi_side == NULL), UNMATCHED
        )
    return file_side, osmi_side


def two_sample_distance(
    file_side: pd.Series, osmi_side: pd.Series, column: str, unit: Unit
) -> ColumnResult:
    """Compute w_d and b of one column as two samples (section 3.4, A6).

    w_d² = Σᵢ (p₁ᵢ − p₂ᵢ)²/Pᵢ, with Pᵢ the pooled share;
    b = √((k − 1)(1/n₁ + 1/n₂)).
    """
    n_1, n_2 = len(file_side), len(osmi_side)
    shares_1 = file_side.value_counts() / n_1
    shares_2 = osmi_side.value_counts() / n_2
    categories = shares_1.index.union(shares_2.index)
    shares_1 = shares_1.reindex(categories, fill_value=0.0)
    shares_2 = shares_2.reindex(categories, fill_value=0.0)
    pooled = (shares_1 * n_1 + shares_2 * n_2) / (n_1 + n_2)
    w_d = math.sqrt(float((((shares_1 - shares_2) ** 2) / pooled).sum()))
    k = len(categories)
    return ColumnResult(
        unit=unit,
        column=column,
        categories=k,
        n_file=n_1,
        n_osmi=n_2,
        w_d=w_d,
        noise_floor=math.sqrt((k - 1) * (1 / n_1 + 1 / n_2)),
    )


def a6_columns(
    records: pd.DataFrame, profiles: pd.DataFrame, osmi: pd.DataFrame
) -> list[ColumnResult]:
    """Compute A6 on every column of the OSMI group, in both units.

    `Timestamp` exists only in the records unit (section 3.4, Units).
    """
    osmi = osmi.copy()
    stamps = pd.to_datetime(osmi[TIMESTAMP], format=OSMI_TIMESTAMP_FORMAT)
    osmi[TIMESTAMP] = stamps.dt.strftime(YEAR_MONTH_FORMAT)
    results = []
    for unit, frame in ((Unit.RECORDS, records), (Unit.PROFILES, profiles)):
        for column in OSMI_GROUP:
            if column not in frame.columns:
                continue
            file_side, osmi_side = a6_categories(frame[column], osmi[column], column)
            results.append(two_sample_distance(file_side, osmi_side, column, unit))
    return results


def a6_unmatched(osmi: pd.DataFrame) -> list[tuple[str, str, int]]:
    """List each OSMI value sent to `UNMATCHED`, with its count (section 3.5)."""
    listed = []
    for column in OSMI_GROUP:
        if column not in DOMAINS:
            continue
        values = osmi[column]
        _, mapped = a6_categories(values, values, column)
        counts = values[mapped == UNMATCHED].value_counts()
        listed += [(column, str(value), int(n)) for value, n in counts.items()]
    return sorted(listed)


def a6_outcome(columns: Iterable[ColumnResult]) -> str:
    """Return discordant, concordant or indeterminate for one unit."""
    columns = list(columns)
    interpretable = [c for c in columns if c.interpretable]
    if any(c.w_d >= SMALL for c in interpretable):
        return "discordant"
    if interpretable:
        return "concordant"
    return "indeterminate"


def a6_outcome_by_unit(columns: Sequence[ColumnResult]) -> dict[str, str]:
    """Return A6's outcome per unit and over both (section 3.4, Units)."""
    timestamp = [c for c in columns if c.column == TIMESTAMP]
    records = a6_outcome(c for c in columns if c.unit is Unit.RECORDS)
    profiles = a6_outcome([c for c in columns if c.unit is Unit.PROFILES] + timestamp)
    combined = records if records == profiles else "indeterminate"
    return {"records": records, "profiles": profiles, "combined": combined}


def care_options_premise_holds(columns: Sequence[ColumnResult]) -> bool:
    """Whether `care_options`' own A6 result is concordant on both units."""
    return all(
        c.result == "concordant" for c in columns if c.column == CARE_OPTIONS
    ) and {c.unit for c in columns if c.column == CARE_OPTIONS} == {
        Unit.RECORDS,
        Unit.PROFILES,
    }


def symptom_profiles(
    frame: pd.DataFrame, columns: Sequence[str] = SYMPTOM_COLUMNS
) -> tuple[pd.DataFrame, int]:
    """Return the trimmed, case-folded rows of `columns` with no null, and the drop.

    The count dropped is of distinct profiles with a null in any of the
    columns (LOG-050, item 2).
    """
    rows = frame[list(columns)].apply(lambda s: s.str.strip().str.casefold())
    has_null = ((rows == "") | (rows == NULL.casefold()) | rows.isna()).any(axis=1)
    dropped = len(rows[has_null].drop_duplicates())
    return rows[~has_null].reset_index(drop=True), dropped


def read_rhmcd(path: Path) -> pd.DataFrame:
    """Read the RHMCD-20 CSV as text; an empty field stays the empty string.

    Raises:
        ExternalDataError: One of the eight symptom columns is missing.
    """
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = [column for column in SYMPTOM_COLUMNS if column not in frame.columns]
    if missing:
        raise ExternalDataError(f"{path}: no column {missing}")
    return frame


def near_keys(profile: tuple[str, ...]) -> list[tuple[str, ...]]:
    """Return the profile with each position in turn replaced by a wildcard."""
    return [profile[:j] + ("\0",) + profile[j + 1 :] for j in range(len(profile))]


def guard(
    r_set: set[tuple[str, ...]],
    marginal_rows: pd.DataFrame,
    f_size: int,
    marginals: Unit,
    columns: Sequence[str] = SYMPTOM_COLUMNS,
) -> Guard:
    """Compute Q = Σ_{p∈R} Πⱼ fⱼ(pⱼ) and log10 G = |F| log10 Q.

    `marginal_rows` holds the rows whose column shares give the fⱼ.
    """
    shares = [
        marginal_rows[column].value_counts(normalize=True).to_dict()
        for column in columns
    ]
    q = sum(
        math.prod(shares[j].get(value, 0.0) for j, value in enumerate(profile))
        for profile in r_set
    )
    log10_g = f_size * math.log10(q) if q > 0 else -math.inf
    return Guard(marginals=marginals, q=q, log10_g=log10_g)


def a10_containment(
    records: pd.DataFrame,
    profiles: pd.DataFrame,
    rhmcd: pd.DataFrame,
    columns: Sequence[str] = SYMPTOM_COLUMNS,
) -> ContainmentResult:
    """Run A10's containment test and its chance model (section 3.4, A10).

    `columns` is the eight symptom columns, or those and `Occupation` for the
    repeated test of the second amendment of 2026-10-29 (section 7).
    """
    record_rows, f_null_excluded = symptom_profiles(records, columns)
    profile_rows, _ = symptom_profiles(profiles, columns)
    r_rows, r_null_excluded = symptom_profiles(rhmcd, columns)
    record_tuples = list(record_rows.itertuples(index=False, name=None))
    f_set = set(record_tuples)
    r_set = set(r_rows.itertuples(index=False, name=None))
    r_near = {key for profile in r_set for key in near_keys(profile)}

    def is_near(profile: tuple[str, ...]) -> bool:
        return profile in r_set or any(key in r_near for key in near_keys(profile))

    f_frame = pd.DataFrame(sorted(f_set), columns=list(columns))
    guards = tuple(
        guard(r_set, rows, len(f_set), unit, columns)
        for unit, rows in (
            (Unit.RECORDS, record_rows),
            (Unit.PROFILES, profile_rows),
            (Unit.SET_F, f_frame),
        )
    )
    return ContainmentResult(
        f_size=len(f_set),
        f_null_excluded=f_null_excluded,
        r_size=len(r_set),
        r_null_excluded=r_null_excluded,
        c=sum(p in r_set for p in f_set) / len(f_set),
        c_1=sum(is_near(p) for p in f_set) / len(f_set),
        records_exact=sum(p in r_set for p in record_tuples) / len(record_tuples),
        records_near=sum(is_near(p) for p in record_tuples) / len(record_tuples),
        guards=guards,
    )


def a10_marginal_comparisons(
    records: pd.DataFrame, profiles: pd.DataFrame, rhmcd: pd.DataFrame
) -> list[ColumnResult]:
    """Compare each symptom column's marginal with RHMCD-20's, as w_d, both units.

    Reported only once exposure is allowed (amendment of 2026-10-29).
    """
    results = []
    for unit, frame in ((Unit.RECORDS, records), (Unit.PROFILES, profiles)):
        for column in SYMPTOM_COLUMNS:
            file_side = frame[column].str.strip().str.casefold()
            r_side = rhmcd[column].str.strip().str.casefold()
            results.append(two_sample_distance(file_side, r_side, column, unit))
    return results


def mapping_rule(a5: str, a6: str, a10: str) -> tuple[str, str]:
    """Return the first rule of R0 to R5 that applies, and its branch.

    A6's "indeterminate" is read as "discordant" (section 3.4, A6).
    """
    if "not obtainable" in (a6, a10):
        return "R0", BOTH_BRANCHES
    if a10 == "confirms":
        return "R1", H1_HOLDS
    if a5 == "contradicts":
        return "R2", H1_DOES_NOT_HOLD
    if a5 == "supports":
        if a6 == "concordant":
            return "R3", H1_HOLDS
        return "R4", BOTH_BRANCHES
    return "R5", BOTH_BRANCHES


def write_csv(
    path: Path, header: Sequence[str], rows: Iterable[Sequence[object]]
) -> None:
    """Write a UTF-8 CSV with a header row and LF line endings."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def measure(value: float) -> str:
    """Format a measure at six decimals."""
    return f"{value:.6f}"


def write_column_results(
    path: Path, columns: Iterable[ColumnResult], with_values: bool
) -> None:
    """Write A6 results, or A10's marginal comparisons, one row per column.

    w_d is written only when `with_values` is set.
    """
    value_header = ("w_d",) if with_values else ()
    write_csv(
        path,
        (
            "unit",
            "column",
            "k",
            "n_file",
            "n_external",
            *value_header,
            "b",
            "interpretable",
            "result",
        ),
        (
            (
                c.unit,
                c.column,
                c.categories,
                c.n_file,
                c.n_osmi,
                *((measure(c.w_d),) if with_values else ()),
                measure(c.noise_floor),
                c.interpretable,
                c.result,
            )
            for c in columns
        ),
    )


def main() -> None:
    """Run A5, A6 and A10, write their CSVs, and print the outcomes and branch."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--with-values", action="store_true")
    arguments = parser.parse_args()

    verify_external(OSMI_PATH, OSMI_SHA256)
    verify_external(RHMCD_PATH, RHMCD_SHA256)
    records = records_unit(SOURCE_PATH)
    profiles = profile_unit(records)
    osmi = read_osmi(OSMI_PATH)
    rhmcd = read_rhmcd(RHMCD_PATH)

    columns = a6_columns(records, profiles, osmi)
    premise = care_options_premise_holds(columns)
    pairs = a5_pairs(records, profiles, care_options_excluded=not premise)
    containment = a10_containment(records, profiles, rhmcd)
    occupation_outcome = "not computed: A10 does not confirm"
    if containment.outcome == "confirms":
        occupation_outcome = a10_containment(
            records, profiles, rhmcd, (*SYMPTOM_COLUMNS, OCCUPATION)
        ).outcome
    a5 = outcome_by_unit(pairs)
    a6 = a6_outcome_by_unit(columns)
    rule, branch = mapping_rule(a5["combined"], a6["combined"], containment.outcome)

    out = CHECKS_DIR
    with_values: bool = arguments.with_values
    out.mkdir(parents=True, exist_ok=True)
    write_csv(
        out / "a5-pairs.csv",
        (
            "unit",
            "column_1",
            "column_2",
            "pair_class",
            "r",
            "c",
            "n",
            *(("v", "w") if with_values else ()),
            "b",
            "interpretable",
            "at_or_above_small",
        ),
        (
            (
                p.unit,
                p.column_1,
                p.column_2,
                p.pair_class,
                p.rows,
                p.columns,
                p.n,
                *((measure(p.cramers_v), measure(p.w)) if with_values else ()),
                measure(p.noise_floor),
                p.interpretable,
                p.at_or_above_small,
            )
            for p in pairs
        ),
    )
    write_column_results(out / "a6-columns.csv", columns, with_values)
    write_csv(
        out / "a6-unmatched.csv", ("column", "osmi_value", "count"), a6_unmatched(osmi)
    )
    summary: list[tuple[str, object]] = [
        ("source_sha256", sha256_of(SOURCE_PATH)),
        ("osmi_sha256", OSMI_SHA256),
        ("rhmcd_sha256", RHMCD_SHA256),
        ("f_size", containment.f_size),
        ("f_null_excluded", containment.f_null_excluded),
        ("r_size", containment.r_size),
        ("r_null_excluded", containment.r_null_excluded),
        ("c", measure(containment.c)),
        ("c_1", measure(containment.c_1)),
        ("records_exact", measure(containment.records_exact)),
        ("records_near", measure(containment.records_near)),
    ]
    for g in containment.guards:
        summary += [
            (f"q_{g.marginals}", f"{g.q:.6e}"),
            (f"log10_g_{g.marginals}", f"{g.log10_g:.3f}"),
            (f"g_below_alpha_{g.marginals}", g.below_alpha),
        ]
    write_csv(out / "a10-summary.csv", ("item", "value"), summary)
    outcomes: list[tuple[str, str, object]] = [
        *(("A5", unit, outcome) for unit, outcome in a5.items()),
        *(("A6", unit, outcome) for unit, outcome in a6.items()),
        ("A6", "care_options premise holds", premise),
        ("A10", "combined", containment.outcome),
        ("A10", "with Occupation", occupation_outcome),
        ("mapping", "rule", rule),
        ("mapping", "branch", branch),
    ]
    write_csv(out / "outcomes.csv", ("check", "scope", "outcome"), outcomes)
    if with_values:
        write_column_results(
            out / "a10-marginal-comparisons.csv",
            a10_marginal_comparisons(records, profiles, rhmcd),
            with_values,
        )
    for check, scope, outcome in outcomes:
        print(f"{check}, {scope}: {outcome}")


if __name__ == "__main__":
    main()
