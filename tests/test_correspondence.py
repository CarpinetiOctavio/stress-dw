import pytest

from stress_dw.correspondence import (
    ADMITTED_STRATA,
    ENTRIES,
    Entry,
    flagged_table,
    reading_list,
    required_cell_rows,
    strata_of,
    summary,
)

BY_PERIOD = Entry(
    "Qx",
    2,
    ("period",),
    ("gender",),
    (("Male",), ("Female",)),
    ("Yes", "No"),
    min_strata=2,
)
ADMITTED = Entry(
    "Qy",
    16,
    ("growing_stress",),
    ("care_options",),
    (("Yes",), ("Not sure",)),
    ("No",),
    strata=(("Yes",), ("Maybe",)),
)


def row(denominator: str = "40", low_n: str = "false", **cuts: str) -> dict[str, str]:
    return {
        **cuts,
        "level": "Yes",
        "numerator": "1",
        "denominator": denominator,
        "rate": "0.025000",
        "low_n": low_n,
    }


def test_a_stratum_exists_only_when_the_output_reports_one_of_its_cells() -> None:
    rows = [row(period="2014-08", gender="Male"), row(period="2014-09", gender="Male")]
    strata = strata_of(BY_PERIOD, rows)
    assert [s.key for s in strata] == [
        (("period", "2014-08"),),
        (("period", "2014-09"),),
    ]
    assert all(s.exists and s.missing == 1 for s in strata)


def test_a_flagged_or_missing_cell_makes_its_stratum_not_readable() -> None:
    rows = [
        row(period="2014-08", gender="Male"),
        row(period="2014-08", gender="Female", denominator="12", low_n="true"),
        row(period="2014-09", gender="Male"),
        row(period="2014-09", gender="Female"),
    ]
    first, second = strata_of(BY_PERIOD, rows)
    assert (first.readable, first.flagged, first.missing) == (False, 1, 0)
    assert second.readable


def test_an_admitted_stratum_with_no_cell_is_absent_and_has_no_required_cells() -> None:
    rows = [
        row(growing_stress="Yes", care_options="Yes"),
        row(growing_stress="Yes", care_options="Not sure"),
    ]
    strata = strata_of(ADMITTED, rows)
    assert [s.exists for s in strata] == [True, False]
    assert len(list(required_cell_rows(ADMITTED, strata))) == 2
    assert reading_list(strata)[-1] == "| growing_stress=Maybe | absent | | |"


def test_fewer_strata_than_the_entry_needs_names_the_design_locus() -> None:
    rows = [
        row(period="2014-08", gender="Male"),
        row(period="2014-08", gender="Female"),
    ]
    text = summary(BY_PERIOD, strata_of(BY_PERIOD, rows))
    assert text.endswith("loci under the cells: reasoning or design")


def test_missing_and_flagged_cells_name_the_data_volume_locus() -> None:
    rows = [
        row(period="2014-08", gender="Male", low_n="true"),
        row(period="2014-09", gender="Male"),
    ]
    text = summary(BY_PERIOD, strata_of(BY_PERIOD, rows))
    assert "missing 2; flagged 1" in text
    assert text.endswith("loci under the cells: data volume")


def test_rows_of_one_cell_that_disagree_on_the_flag_are_rejected() -> None:
    rows = [
        row(period="2014-08", gender="Male"),
        row(period="2014-08", gender="Male", low_n="true"),
    ]
    with pytest.raises(ValueError, match="2014-08"):
        strata_of(BY_PERIOD, rows)


def test_only_flagged_cells_are_listed() -> None:
    rows = [
        row(period="2014-08", gender="Male", denominator="12", low_n="true"),
        row(period="2014-08", gender="Female"),
    ]
    lines = flagged_table(BY_PERIOD, strata_of(BY_PERIOD, rows))
    assert lines[2:] == ["| 2014-08 | Male | 12 | flagged |"]


def test_q7_1_requires_its_eight_cells_whether_or_not_they_occur() -> None:
    (entry,) = (e for e in ENTRIES if e.question == "Q7.1")
    (stratum,) = strata_of(entry, [])
    assert stratum.exists
    assert stratum.missing == 8
    assert ADMITTED_STRATA[0] == ("Yes", "true", "Yes")


def test_q3_reads_each_grouping_set_separately() -> None:
    entries = [e for e in ENTRIES if e.question == "Q3"]
    assert [e.grouping_set for e in entries] == [
        "occupation, country",
        "occupation, region",
    ]
    country = row(occupation="Business", country="Chile", region="")
    country["grouping_set"] = "occupation, country"
    (stratum,) = strata_of(entries[0], [country])
    assert stratum.missing == 4
    assert strata_of(entries[1], [country]) == []
