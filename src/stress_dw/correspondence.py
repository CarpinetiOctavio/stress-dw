"""Cell status of each question's required cells, for the evidence document.

Applies the cell rules of docs/audit/correspondence-criteria.md (sections 4 to
6) to the published indicator output in `EVIDENCE_DIR`: for each question, the
strata that exist, the required cells, and whether each is present and flagged
by `low_n`. It reads only the published CSVs, never the database.

`required-cells.csv` holds one row per required cell. The run also prints, in
Markdown, each question's counts, its reading list where its entry defines
strata, and the cells its criteria read, for the evidence document.

Run from the repository root: `uv run python -m stress_dw.correspondence`.
"""

import csv
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from itertools import product

from stress_dw.domains import DOMAINS
from stress_dw.evidence import EVIDENCE_DIR, indicator_file, write_rows

REQUIRED_CELLS_FILE = "required-cells.csv"
REQUIRED_CELLS_HEADER = (
    "question",
    "indicator",
    "stratum",
    "cell",
    "present",
    "denominator",
    "low_n",
)

TRUE = "true"
FALSE = "false"
YES = "Yes"
NOT_SURE = "Not sure"
GENDER = "gender"
GROWING_STRESS = "growing_stress"
OCCUPATION = "occupation"
COUNTRY = "country"
REGION = "region"
SYMPTOM_CLUSTER = "symptom_cluster"
CARE_OPTIONS = "care_options"

GENDERS = DOMAINS["Gender"]
STRESS_LEVELS = DOMAINS["Growing_Stress"]
OCCUPATIONS = DOMAINS["Occupation"]

# Q7.1 and Q7.2: the (`growing_stress`, `symptom_cluster`, `care_options`)
# combinations the population admits, headline stratum first, then by
# `growing_stress` (Yes, Maybe, No), `symptom_cluster` (true, false) and
# `care_options` (Yes, Not sure) (criteria, Q7.1, Cells; Q7.2, Reading list).
ADMITTED_STRATA: tuple[tuple[str, ...], ...] = tuple(
    (stress, cluster, care)
    for stress, cluster in (
        (YES, TRUE),
        (YES, FALSE),
        ("Maybe", TRUE),
        ("No", TRUE),
    )
    for care in (YES, NOT_SURE)
)


@dataclass(frozen=True)
class Entry:
    """The cell rules of one indicator under one question's criteria.

    `cell_cuts` and `cells` name the required cells within each stratum.
    `strata` lists the admitted strata in reading order; `None` means every
    stratum the output reports, in sort order. An entry without
    `stratum_cuts` has one stratum, which always exists. `min_strata` is the
    fewest strata the determination needs. `levels` are the levels whose
    rates the criteria read; empty for pattern B.
    """

    question: str
    indicator: int
    stratum_cuts: tuple[str, ...]
    cell_cuts: tuple[str, ...]
    cells: tuple[tuple[str, ...], ...]
    levels: tuple[str, ...]
    strata: tuple[tuple[str, ...], ...] | None = None
    min_strata: int = 0
    grouping_set: str | None = None


def by_gender(question: str, indicator: int) -> Entry:
    """Q1 and Q2: by period, the two `Gender` cells, three level rates."""
    return Entry(
        question,
        indicator,
        ("period",),
        (GENDER,),
        tuple((g,) for g in GENDERS),
        (YES, "No", "Maybe"),
        min_strata=2,
    )


def by_occupation(stratum: str) -> Entry:
    """Q3: the five `Occupation` cells in each country, or in each region."""
    return Entry(
        "Q3",
        6,
        (stratum,),
        (OCCUPATION,),
        tuple((o,) for o in OCCUPATIONS),
        (),
        min_strata=2 if stratum == REGION else 0,
        grouping_set=f"{OCCUPATION}, {stratum}",
    )


def by_time_indoors(indicator: int, levels: tuple[str, ...]) -> Entry:
    """Q5: the five `days_indoors` cells, shared by indicators 9 to 11."""
    return Entry(
        "Q5",
        indicator,
        (),
        ("days_indoors",),
        tuple((d,) for d in DOMAINS["Days_Indoors"]),
        levels,
    )


ENTRIES: tuple[Entry, ...] = (
    by_gender("Q1", 2),
    by_gender("Q2", 4),
    by_occupation(COUNTRY),
    by_occupation(REGION),
    Entry(
        "Q4",
        7,
        (),
        (GENDER, GROWING_STRESS),
        tuple(product(GENDERS, STRESS_LEVELS)),
        (YES,),
    ),
    by_time_indoors(9, STRESS_LEVELS),
    by_time_indoors(10, DOMAINS["Mood_Swings"]),
    by_time_indoors(11, DOMAINS["Social_Weakness"]),
    Entry(
        "Q6",
        12,
        (COUNTRY,),
        (GROWING_STRESS, OCCUPATION, GENDER),
        tuple(product(STRESS_LEVELS, OCCUPATIONS, GENDERS)),
        (YES, NOT_SURE, "No"),
        min_strata=2,
    ),
    Entry("Q7", 14, (), (GROWING_STRESS,), tuple((s,) for s in STRESS_LEVELS), (YES,)),
    Entry(
        "Q7.1",
        15,
        (),
        (GROWING_STRESS, SYMPTOM_CLUSTER, CARE_OPTIONS),
        ADMITTED_STRATA,
        (YES,),
    ),
    Entry(
        "Q7.2",
        16,
        (GROWING_STRESS, SYMPTOM_CLUSTER, CARE_OPTIONS),
        ("mental_health_interview",),
        tuple((m,) for m in DOMAINS["mental_health_interview"]),
        ("No",),
        strata=ADMITTED_STRATA,
    ),
)


@dataclass(frozen=True)
class Cell:
    """One required cell: its key, and its rows in the output, if any."""

    key: tuple[tuple[str, str], ...]
    rows: tuple[dict[str, str], ...]

    @property
    def present(self) -> bool:
        """Whether the output reports the cell."""
        return bool(self.rows)

    @property
    def flagged(self) -> bool:
        """Whether the cell is present and flagged by `low_n`."""
        return self.present and self.rows[0]["low_n"] == TRUE

    @property
    def denominator(self) -> str:
        """The cell's denominator, or an empty string when it is missing."""
        return self.rows[0]["denominator"] if self.rows else ""


@dataclass(frozen=True)
class Stratum:
    """One admitted or reported stratum and its required cells."""

    key: tuple[tuple[str, str], ...]
    exists: bool
    cells: tuple[Cell, ...]

    @property
    def missing(self) -> int:
        """The number of required cells the output does not report."""
        return sum(not c.present for c in self.cells)

    @property
    def flagged(self) -> int:
        """The number of required cells flagged by `low_n`."""
        return sum(c.flagged for c in self.cells)

    @property
    def readable(self) -> bool:
        """Whether every required cell is present and unflagged."""
        return self.exists and not self.missing and not self.flagged


def label(key: Iterable[tuple[str, str]]) -> str:
    """Write a cell or stratum key as `cut=value` pairs."""
    return "; ".join(f"{cut}={value}" for cut, value in key)


def group_rows(
    rows: Iterable[dict[str, str]], cuts: Sequence[str]
) -> dict[tuple[str, ...], tuple[dict[str, str], ...]]:
    """Group output rows by their values on `cuts`.

    Raises:
        ValueError: the rows of one cell disagree on the denominator or on
            `low_n`, which pattern A and pattern C rule out.
    """
    groups: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for row in rows:
        groups.setdefault(tuple(row[c] for c in cuts), []).append(row)
    for values, members in groups.items():
        if len({(r["denominator"], r["low_n"]) for r in members}) > 1:
            raise ValueError(f"cell {values}: rows disagree on denominator or low_n")
    return {values: tuple(members) for values, members in groups.items()}


def strata_of(entry: Entry, rows: Sequence[dict[str, str]]) -> list[Stratum]:
    """Apply `entry`'s cell rules to an indicator's output rows."""
    if entry.grouping_set is not None:
        rows = [r for r in rows if r["grouping_set"] == entry.grouping_set]
    groups = group_rows(rows, entry.stratum_cuts + entry.cell_cuts)
    reported = {values[: len(entry.stratum_cuts)] for values in groups}
    if not entry.stratum_cuts:
        admitted: Sequence[tuple[str, ...]] = [()]
    elif entry.strata is not None:
        admitted = entry.strata
    else:
        admitted = sorted(reported)
    strata = []
    for stratum in admitted:
        cells = tuple(
            Cell(
                tuple(
                    zip(
                        entry.stratum_cuts + entry.cell_cuts,
                        stratum + cell,
                        strict=True,
                    )
                ),
                groups.get(stratum + cell, ()),
            )
            for cell in entry.cells
        )
        exists = not entry.stratum_cuts or stratum in reported
        strata.append(
            Stratum(tuple(zip(entry.stratum_cuts, stratum, strict=True)), exists, cells)
        )
    return strata


def read_output(number: int) -> list[dict[str, str]]:
    """Read indicator `number`'s published output."""
    with (EVIDENCE_DIR / indicator_file(number)).open(encoding="utf-8") as file:
        return list(csv.DictReader(file))


def required_cell_rows(
    entry: Entry, strata: Iterable[Stratum]
) -> Iterator[tuple[str | int, ...]]:
    """Yield the `required-cells.csv` rows of `entry`, existing strata only."""
    for stratum in strata:
        if not stratum.exists:
            continue
        for cell in stratum.cells:
            yield (
                entry.question,
                entry.indicator,
                label(stratum.key),
                label(cell.key),
                TRUE if cell.present else FALSE,
                cell.denominator,
                (TRUE if cell.flagged else FALSE) if cell.present else "",
            )


def summary(entry: Entry, strata: Sequence[Stratum]) -> str:
    """Count the strata and required cells of `entry`, and name its loci."""
    existing = [s for s in strata if s.exists]
    cells = [c for s in existing for c in s.cells]
    missing = sum(not c.present for c in cells)
    flagged = sum(c.flagged for c in cells)
    loci = []
    if missing or flagged:
        loci.append("data volume")
    if len(existing) < entry.min_strata:
        loci.append("reasoning or design")
    scope = f" ({entry.grouping_set})" if entry.grouping_set else ""
    return (
        f"{entry.question}, indicator {entry.indicator}{scope}: "
        f"strata {len(existing)}; required cells {len(cells)}; "
        f"present {len(cells) - missing}; missing {missing}; flagged {flagged}; "
        f"loci under the cells: {', '.join(loci) or 'none'}"
    )


def reading_list(strata: Sequence[Stratum]) -> list[str]:
    """Write the reading list of a stratified entry as a Markdown table."""
    lines = ["| Stratum | Reading | Missing | Flagged |", "|---|---|---|---|"]
    for s in strata:
        if not s.exists:
            lines.append(f"| {label(s.key)} | absent | | |")
            continue
        reading = "readable" if s.readable else "not readable"
        lines.append(f"| {label(s.key)} | {reading} | {s.missing} | {s.flagged} |")
    return lines


def cell_table(entry: Entry, strata: Sequence[Stratum]) -> list[str]:
    """Write the cells `entry`'s criteria read as a Markdown table.

    A level rate is written as numerator (rate). A level with no row in a
    present cell has numerator 0 (criteria, section 5, item 5).
    """
    cuts = entry.stratum_cuts + entry.cell_cuts
    head = [*cuts, "denominator", *entry.levels, "low_n"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for stratum in (s for s in strata if s.exists):
        for cell in stratum.cells:
            values = [value for _, value in cell.key]
            if not cell.present:
                rest = ["missing"] + [""] * (len(entry.levels) + 1)
            else:
                by_level = {r["level"]: r for r in cell.rows}
                rates = [
                    f"{by_level[v]['numerator']} ({by_level[v]['rate']})"
                    if v in by_level
                    else "0 (no row)"
                    for v in entry.levels
                ]
                flag = "**flagged**" if cell.flagged else FALSE
                rest = [cell.denominator, *rates, flag]
            lines.append("| " + " | ".join(values + rest) + " |")
    return lines


def flagged_table(entry: Entry, strata: Sequence[Stratum]) -> list[str]:
    """List the flagged required cells of `entry` as a Markdown table."""
    flagged = [c for s in strata for c in s.cells if c.flagged]
    if not flagged:
        return ["No required cell is flagged."]
    cuts = entry.stratum_cuts + entry.cell_cuts
    lines = ["| " + " | ".join([*cuts, "denominator", "low_n"]) + " |"]
    lines.append("|" + "---|" * (len(cuts) + 2))
    for cell in flagged:
        values = [value for _, value in cell.key]
        lines.append("| " + " | ".join([*values, cell.denominator, "flagged"]) + " |")
    return lines


# Questions whose required cells are too many to list: counts, reading list
# and the flagged cells only.
COUNTED_QUESTIONS = frozenset({"Q3", "Q6"})


def main() -> None:
    """Write `required-cells.csv` and print each question's Markdown."""
    rows: list[tuple[str | int, ...]] = []
    for entry in ENTRIES:
        strata = strata_of(entry, read_output(entry.indicator))
        rows.extend(required_cell_rows(entry, strata))
        print(f"\n## {summary(entry, strata)}\n")
        if entry.stratum_cuts:
            print("\n".join(reading_list(strata)), "\n")
        if entry.question not in COUNTED_QUESTIONS:
            print("\n".join(cell_table(entry, strata)))
        else:
            print("\n".join(flagged_table(entry, strata)))
    write_rows(EVIDENCE_DIR / REQUIRED_CELLS_FILE, REQUIRED_CELLS_HEADER, rows)
    print(f"\nrequired cells written: {len(rows)}")


if __name__ == "__main__":
    main()
