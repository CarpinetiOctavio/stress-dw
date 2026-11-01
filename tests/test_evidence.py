import pandas as pd
import pytest

from stress_dw.evidence import (
    matches,
    numbers_in,
    rounded,
    search_terms,
    serialize,
    serialize_cell,
)


def frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "country": ["Chile", None, "Côte, d'Ivoire"],
            "numerator": [1, 1234, 0],
            "denominator": [3, 290051, 7],
            "rate": [1 / 3, 0.75, 0.0],
            "low_n": [True, False, True],
        }
    )


def test_serialization_keeps_column_order_and_ends_with_a_newline() -> None:
    text = serialize(frame()).decode("utf-8")
    lines = text.split("\n")
    assert lines[0] == "country,numerator,denominator,rate,low_n"
    assert text.endswith("\n")
    assert not text.endswith("\n\n")
    assert "\r" not in text


def test_serialization_writes_null_as_an_empty_field_and_booleans_in_lowercase() -> (
    None
):
    lines = serialize(frame()).decode("utf-8").split("\n")
    assert lines[1] == "Chile,1,3,0.333333,true"
    assert lines[2] == ",1234,290051,0.750000,false"


def test_serialization_quotes_only_fields_that_require_it() -> None:
    lines = serialize(frame()).decode("utf-8").split("\n")
    assert lines[3] == '"Côte, d\'Ivoire",0,7,0.000000,true'


def test_serialization_is_utf8() -> None:
    assert "Côte".encode() in serialize(frame())


def test_rates_round_half_away_from_zero_on_the_exact_value() -> None:
    assert rounded(0.125, 2) == "0.13"
    assert rounded(-0.125, 2) == "-0.13"
    # 0.145 is stored as 0.14499999999999999; the exact value rounds down.
    assert rounded(0.145, 2) == "0.14"


def test_a_float_outside_the_rate_columns_is_rejected() -> None:
    with pytest.raises(TypeError, match="numerator"):
        serialize_cell("numerator", 1.0)


def test_search_terms_cover_counts_above_the_floor_in_both_forms() -> None:
    terms = search_terms({1: serialize(frame())})
    assert terms[("290051", False)] == {1}
    assert terms[("290,051", False)] == {1}
    assert terms[("1234", False)] == {1}
    assert ("7", False) not in terms


def test_search_terms_cover_rates_as_fractions_and_percentages() -> None:
    terms = search_terms({4: serialize(frame())})
    for form in ("0.333333", "0.3333", "0.333", "33.3", "33.33"):
        assert terms[(form, False)] == {4}
    assert terms[("33", True)] == {4}
    assert ("33", False) not in terms


def test_values_are_not_matched_inside_words_hashes_or_longer_numbers() -> None:
    terms = search_terms({1: serialize(frame())})
    text = "a290051 290051b 1290051 2900510 0.3333x 10.3333 3.3333.1"
    assert list(matches(text, terms)) == []


def test_version_like_strings_yield_no_numbers() -> None:
    assert list(numbers_in("v3.12 4.2.1 sha 8b67c52")) == []


def test_a_csv_row_is_split_into_its_fields() -> None:
    assert list(numbers_in("290051,1234,0.333")) == [
        ("290051", False),
        ("1234", False),
        ("0.333", False),
    ]


def test_a_number_with_thousands_commas_stays_whole() -> None:
    assert list(numbers_in("of 290,051 records.")) == [("290,051", False)]


def test_a_whole_percentage_matches_only_with_the_percent_sign() -> None:
    terms = search_terms({4: serialize(frame())})
    assert list(matches("33% of rows", terms)) == [("33%", {4})]
    assert list(matches("33 rows", terms)) == []
