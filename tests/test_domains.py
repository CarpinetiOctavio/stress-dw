from collections import Counter

from stress_dw.domains import COUNTRY_REGION, DOMAINS


def test_the_mapping_has_the_35_countries_in_the_specified_region_counts() -> None:
    # docs/specification/country-region-mapping.md: 2 + 19 + 6 + 2 + 2 + 4.
    assert Counter(COUNTRY_REGION.values()) == {
        "Northern America": 2,
        "Europe": 19,
        "Asia": 6,
        "Oceania": 2,
        "Africa": 2,
        "Latin America and the Caribbean": 4,
    }


def test_the_country_domain_is_the_mapping() -> None:
    assert set(DOMAINS["Country"]) == set(COUNTRY_REGION)


def test_no_domain_holds_two_literals_differing_only_in_case() -> None:
    for domain in DOMAINS.values():
        assert len({literal.lower() for literal in domain}) == len(domain)
