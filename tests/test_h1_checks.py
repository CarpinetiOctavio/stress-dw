import math
from pathlib import Path

import pandas as pd
import pytest

from stress_dw.h1_checks import (
    NULL,
    UNMATCHED,
    ColumnResult,
    ContainmentResult,
    Guard,
    PairResult,
    Unit,
    a5_outcome,
    a6_categories,
    a6_outcome,
    association,
    care_options_premise_holds,
    chi_squared,
    guard,
    harmonize_unmodeled,
    mapping_rule,
    outcome_by_unit,
    pair_class,
    read_osmi,
    two_sample_distance,
)


def pair(
    pair_class: str, w: float, noise_floor: float = 0.01, unit: Unit = Unit.RECORDS
) -> PairResult:
    return PairResult(unit, "a", "b", pair_class, 2, 2, 1000, w, w, noise_floor)


def column(
    name: str, w_d: float, noise_floor: float = 0.01, unit: Unit = Unit.RECORDS
) -> ColumnResult:
    return ColumnResult(unit, name, 2, 1000, 1000, w_d, noise_floor)


def unmodeled_frame(**overrides: list[str]) -> pd.DataFrame:
    columns = (
        "self_employed",
        "Changes_Habits",
        "Mental_Health_History",
        "Work_Interest",
    )
    size = len(next(iter(overrides.values())))
    return pd.DataFrame({c: overrides.get(c, ["No"] * size) for c in columns})


def test_case_variants_merge_under_their_most_frequent_form() -> None:
    frame = unmodeled_frame(Work_Interest=["no", "No ", "No", " Maybe"])
    assert list(harmonize_unmodeled(frame)["Work_Interest"]) == [
        "No",
        "No",
        "No",
        "Maybe",
    ]


def test_a_tie_between_case_forms_goes_to_the_first_by_code_point() -> None:
    frame = unmodeled_frame(Work_Interest=["yes", "Yes"])
    assert list(harmonize_unmodeled(frame)["Work_Interest"]) == ["Yes", "Yes"]


def test_an_empty_unmodeled_value_becomes_the_null_category() -> None:
    frame = unmodeled_frame(self_employed=["", " ", "Yes"])
    assert list(harmonize_unmodeled(frame)["self_employed"]) == [NULL, NULL, "Yes"]


def test_cramers_v_of_a_2x2_table_equals_the_absolute_phi_coefficient() -> None:
    a, b, c, d = 30, 10, 20, 40
    frame = pd.DataFrame(
        {
            "x": ["1"] * (a + b) + ["2"] * (c + d),
            "y": ["1"] * a + ["2"] * b + ["1"] * c + ["2"] * d,
        }
    )
    phi = (a * d - b * c) / math.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    result = association(frame, "x", "y", Unit.RECORDS, care_options_excluded=False)
    assert result.cramers_v == pytest.approx(abs(phi))
    assert result.noise_floor == pytest.approx(math.sqrt(1 / 99))


def test_cramers_v_divides_w_by_the_smaller_dimension_minus_one() -> None:
    frame = pd.DataFrame({"x": list("aabbcc") * 10, "y": list("pqpqrr") * 10})
    result = association(frame, "x", "y", Unit.RECORDS, care_options_excluded=False)
    assert (result.rows, result.columns) == (3, 3)
    assert result.cramers_v == pytest.approx(result.w / math.sqrt(2))
    assert result.noise_floor == pytest.approx(math.sqrt(4 / 59))


def test_w_d_equals_v_of_the_2xk_table_over_root_pi_one_minus_pi() -> None:
    file_side = pd.Series(["a"] * 70 + ["b"] * 20 + ["c"] * 10)
    osmi_side = pd.Series(["a"] * 20 + ["b"] * 15 + ["c"] * 5)
    result = two_sample_distance(file_side, osmi_side, "x", Unit.RECORDS)
    table = pd.crosstab(
        pd.Series(["file"] * 100 + ["osmi"] * 40),
        pd.concat([file_side, osmi_side], ignore_index=True),
    )
    v = math.sqrt(chi_squared(table) / 140)
    pi = 40 / 140
    assert result.w_d == pytest.approx(v / math.sqrt(pi * (1 - pi)))
    assert result.noise_floor == pytest.approx(math.sqrt(2 * (1 / 100 + 1 / 40)))


def test_w_d_depends_on_the_ratio_of_sample_sizes_only_through_pooled_shares() -> None:
    file_side = pd.Series(["a"] * 50 + ["b"] * 50)
    osmi_side = pd.Series(["a"] * 30 + ["b"] * 10)
    larger_file = pd.Series(["a"] * 500 + ["b"] * 500)
    small = two_sample_distance(file_side, osmi_side, "x", Unit.RECORDS)
    large = two_sample_distance(larger_file, osmi_side, "x", Unit.RECORDS)
    # p₁ = (0.5, 0.5), p₂ = (0.75, 0.25): w_d² lies between Σd²/p₂ and Σd²/p₁.
    lower = math.sqrt(0.25**2 / 0.5 * 2)
    upper = math.sqrt(0.25**2 * (1 / 0.75 + 1 / 0.25))
    for result in (small, large):
        assert lower <= result.w_d <= upper
    assert small.w_d != pytest.approx(large.w_d)


def test_occupation_pairs_are_excluded_from_aggregation() -> None:
    assert pair_class("Occupation", "Gender", False) == "excluded: Occupation"
    assert pair_class("Occupation", "Mood_Swings", True) == "excluded: Occupation"


def test_care_options_pairs_are_excluded_only_when_its_premise_fails() -> None:
    assert pair_class("care_options", "Mood_Swings", False) == "cross"
    assert pair_class("care_options", "Mood_Swings", True) == "excluded: care_options"


def test_pairs_are_classed_by_group() -> None:
    assert pair_class("Gender", "Country", False) == "within-OSMI"
    assert pair_class("Gender", "Mood_Swings", False) == "cross"
    assert pair_class("Mood_Swings", "Work_Interest", False) == "within other group"


def test_a5_contradicts_on_one_interpretable_cross_pair_at_small() -> None:
    assert a5_outcome([pair("cross", 0.10), pair("cross", 0.01)]) == "contradicts"


def test_a5_supports_when_cross_pairs_are_below_small_and_osmi_has_structure() -> None:
    assert a5_outcome([pair("cross", 0.05), pair("within-OSMI", 0.20)]) == "supports"


def test_a5_is_indeterminate_when_a_cross_pair_is_uninterpretable() -> None:
    pairs = [pair("cross", 0.30, noise_floor=0.06), pair("within-OSMI", 0.20)]
    assert a5_outcome(pairs) == "indeterminate"


def test_a5_ignores_excluded_pairs() -> None:
    pairs = [
        pair("excluded: Occupation", 0.90),
        pair("within other group", 0.90),
        pair("cross", 0.01),
        pair("within-OSMI", 0.20),
    ]
    assert a5_outcome(pairs) == "supports"


def test_a5_is_indeterminate_when_the_two_units_differ() -> None:
    pairs = [
        pair("cross", 0.20, unit=Unit.RECORDS),
        pair("cross", 0.01, unit=Unit.PROFILES),
        pair("within-OSMI", 0.20, unit=Unit.PROFILES),
    ]
    assert outcome_by_unit(pairs) == {
        "records": "contradicts",
        "profiles": "supports",
        "combined": "indeterminate",
    }


def test_an_osmi_value_matching_no_label_goes_to_unmatched() -> None:
    file_side, osmi_side = a6_categories(
        pd.Series(["Male", "Female"]), pd.Series([" male", "M", NULL]), "Gender"
    )
    assert list(file_side) == ["male", "female"]
    assert list(osmi_side) == ["male", UNMATCHED, NULL]


def test_a_column_without_domain_is_only_trimmed_and_case_folded() -> None:
    _, osmi_side = a6_categories(
        pd.Series(["Yes"]), pd.Series([" YES", "Perhaps"]), "self_employed"
    )
    assert list(osmi_side) == ["yes", "perhaps"]


def test_a6_is_discordant_on_one_interpretable_column_at_small() -> None:
    assert a6_outcome([column("a", 0.10), column("b", 0.01)]) == "discordant"


def test_a6_is_indeterminate_when_no_column_is_interpretable() -> None:
    assert a6_outcome([column("a", 0.01, noise_floor=0.05)]) == "indeterminate"


def test_care_options_premise_needs_concordance_on_both_units() -> None:
    both = [
        column("care_options", 0.01, unit=Unit.RECORDS),
        column("care_options", 0.01, unit=Unit.PROFILES),
    ]
    one = [
        column("care_options", 0.01, unit=Unit.RECORDS),
        column("care_options", 0.20, unit=Unit.PROFILES),
    ]
    assert care_options_premise_holds(both)
    assert not care_options_premise_holds(one)


@pytest.mark.parametrize(
    ("a5", "a6", "a10", "expected"),
    [
        (
            "contradicts",
            "not obtainable",
            "confirms",
            ("R0", "both, without resolving"),
        ),
        (
            "contradicts",
            "discordant",
            "not obtainable",
            ("R0", "both, without resolving"),
        ),
        ("contradicts", "discordant", "confirms", ("R1", "H1 holds")),
        ("contradicts", "concordant", "does not confirm", ("R2", "H1 does not hold")),
        ("supports", "concordant", "does not confirm", ("R3", "H1 holds")),
        (
            "supports",
            "discordant",
            "does not confirm",
            ("R4", "both, without resolving"),
        ),
        (
            "supports",
            "indeterminate",
            "does not confirm",
            ("R4", "both, without resolving"),
        ),
        (
            "indeterminate",
            "concordant",
            "does not confirm",
            ("R5", "both, without resolving"),
        ),
    ],
)
def test_the_first_applicable_rule_sets_the_branch(
    a5: str, a6: str, a10: str, expected: tuple[str, str]
) -> None:
    assert mapping_rule(a5, a6, a10) == expected


def test_q_sums_the_product_of_marginal_shares_over_r() -> None:
    columns = (
        "Days_Indoors",
        "Growing_Stress",
        "Changes_Habits",
        "Mental_Health_History",
        "Mood_Swings",
        "Coping_Struggles",
        "Work_Interest",
        "Social_Weakness",
    )
    rows = pd.DataFrame([["a"] * 8, ["a"] * 7 + ["b"]], columns=list(columns))
    result = guard({("a",) * 8}, rows, f_size=3, marginals=Unit.SET_F)
    assert result.q == pytest.approx(0.5)
    assert result.log10_g == pytest.approx(3 * math.log10(0.5))
    assert not result.below_alpha


def containment(c: float, below: tuple[bool, bool, bool]) -> ContainmentResult:
    guards = tuple(
        Guard(unit, 0.1, -3.0 if b else -1.0)
        for unit, b in zip(
            (Unit.RECORDS, Unit.PROFILES, Unit.SET_F), below, strict=True
        )
    )
    return ContainmentResult(10, 0, 20, 0, c, c, c, c, guards)


def test_a10_confirms_only_if_g_is_below_alpha_under_all_three_marginals() -> None:
    assert containment(1.0, (True, True, True)).outcome == "confirms"
    assert containment(1.0, (True, False, True)).outcome == "does not confirm"
    assert containment(0.99, (True, True, True)).outcome == "does not confirm"


def test_the_osmi_arff_reader_handles_quotes_escapes_and_missing_values(
    tmp_path: Path,
) -> None:
    names = (
        "Timestamp",
        "Gender",
        "Country",
        "self_employed",
        "family_history",
        "treatment",
        "mental_health_interview",
        "care_options",
        "comments",
    )
    header = "\n".join(f"@ATTRIBUTE {name} STRING" for name in names)
    row = (
        "'2014-08-27 11:29:31',Female,'United States',?,No,Yes,No,'Not sure',"
        "'Don\\'t, ok'"
    )
    path = tmp_path / "osmi.arff"
    path.write_text(f"@RELATION x\n{header}\n@DATA\n{row}\n", encoding="utf-8")
    frame = read_osmi(path)
    assert frame.loc[0, "Country"] == "United States"
    assert frame.loc[0, "self_employed"] == NULL
    assert frame.loc[0, "comments"] == "Don't, ok"
