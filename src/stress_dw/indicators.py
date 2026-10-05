"""Query layer: the sixteen indicators of docs/specification/indicators.md.

Each indicator is one statement in `sql/indicators/indicator_NN.sql`, an
instance of one of the three patterns of docs/specification/patterns.md, run
against `fact_response` and the dimensions. Nothing is stored: every call
computes its result at query time.

Output columns follow patterns.md: the indicator's cut values; `level`
(patterns A and C); `numerator`; `denominator`; `rate`; `low_n`. Indicators 5
and 6 add `grouping_set`, naming which of their two grouping sets a row
belongs to; indicator 10 adds `headline_rate`, its (`Medium` + `High`) share.
Indicator 8 keeps only the `Yes` level, per indicators.md.
"""

from dataclasses import dataclass
from importlib.resources import files

import duckdb
import pandas as pd

# patterns.md#reporting-rules: the default of `low_n_threshold`.
DEFAULT_LOW_N_THRESHOLD = 30

SYMPTOM_CLUSTER_CAVEAT = (
    "Uses symptom_cluster; see its validity caveat: "
    "docs/specification/definitions.md#symptom_cluster"
)


@dataclass(frozen=True)
class Indicator:
    """An indicator's identity and shape, per indicators.md."""

    number: int
    name: str
    pattern: str
    cuts: tuple[str, ...]
    uses_symptom_cluster: bool = False


INDICATORS: dict[int, Indicator] = {
    indicator.number: indicator
    for indicator in (
        Indicator(1, "Stress-recognition (count)", "A", ()),
        Indicator(2, "Stress-recognition rate", "A", ("period", "gender")),
        Indicator(3, "Family-history/stress coexistence (count)", "A", ()),
        Indicator(
            4, "Family-history/stress coexistence rate", "A", ("gender", "period")
        ),
        Indicator(
            5,
            "Stress/coping-difficulty co-occurrence (count)",
            "B",
            ("occupation", "country", "region"),
        ),
        Indicator(
            6,
            "Stress/coping-difficulty co-occurrence rate",
            "B",
            ("occupation", "country", "region"),
        ),
        Indicator(
            7, "Lifetime treatment-seeking rate", "C", ("gender", "growing_stress")
        ),
        Indicator(
            8, "Lifetime treatment-seeking (count)", "C", ("gender", "growing_stress")
        ),
        Indicator(
            9,
            "Explicit stress-recognition rate by time indoors",
            "A",
            ("days_indoors",),
        ),
        Indicator(
            10, "Elevated mood-swings rate by time indoors", "A", ("days_indoors",)
        ),
        Indicator(11, "Social-weakness rate by time indoors", "A", ("days_indoors",)),
        Indicator(
            12,
            "Care-options response rate",
            "A",
            ("growing_stress", "country", "occupation", "gender"),
        ),
        Indicator(
            13,
            "Care-options response (count)",
            "A",
            ("growing_stress", "country", "occupation", "gender"),
        ),
        Indicator(
            14,
            "Lifetime treatment-seeking rate by explicit-recognition level, "
            "within the convergent-symptom population",
            "C",
            ("growing_stress",),
            uses_symptom_cluster=True,
        ),
        Indicator(
            15,
            "Lifetime treatment-seeking rate by care-options response",
            "C",
            ("growing_stress", "symptom_cluster", "care_options"),
            uses_symptom_cluster=True,
        ),
        Indicator(
            16,
            "Lifetime no-treatment rate by stated disclosure willingness",
            "C",
            (
                "growing_stress",
                "symptom_cluster",
                "care_options",
                "mental_health_interview",
            ),
            uses_symptom_cluster=True,
        ),
    )
}


@dataclass(frozen=True)
class IndicatorResult:
    """An indicator's output rows, with the caveats that must accompany them."""

    indicator: Indicator
    rows: pd.DataFrame
    caveats: tuple[str, ...]


def run_indicator(
    connection: duckdb.DuckDBPyConnection,
    number: int,
    low_n_threshold: int = DEFAULT_LOW_N_THRESHOLD,
) -> IndicatorResult:
    """Compute indicator `number` against a loaded warehouse.

    Assumes the eight dimensions and `fact_response` are loaded. `low_n` is
    true for a row whose `denominator` is below `low_n_threshold`; no row is
    suppressed (patterns.md#reporting-rules).

    Raises:
        ValueError: `number` is not an indicator of indicators.md.
    """
    if number not in INDICATORS:
        raise ValueError(f"no indicator {number}; indicators are numbered 1 to 16")
    indicator = INDICATORS[number]
    query = (
        files("stress_dw") / "sql" / "indicators" / f"indicator_{number:02d}.sql"
    ).read_text()
    rows = connection.execute(query, [low_n_threshold]).df()
    caveats = (SYMPTOM_CLUSTER_CAVEAT,) if indicator.uses_symptom_cluster else ()
    return IndicatorResult(indicator=indicator, rows=rows, caveats=caveats)
