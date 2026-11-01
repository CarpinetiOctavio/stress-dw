"""Query-time cost of the sixteen indicators (DC-21).

ADR-0007 computes every indicator at query time and leaves its cost at the
volume of the staged records as an assumption to check once the pipeline
exists. This module measures it and states no threshold, since ADR-0007 sets
none. One full reload goes into `DATABASE`; each indicator is then run once to
warm up and `RUNS` times measured, through `run_indicator`, so each time
covers reading the query, executing it and building the output frame.

`query-time.csv`, in `EVIDENCE_DIR`, holds the median and the range of the
measured runs, in milliseconds. The run prints the environment it was
measured in.

Run from the repository root: `uv run python -m stress_dw.query_time`.
"""

import os
import platform
import statistics
import time
from collections.abc import Callable
from functools import partial
from pathlib import Path

import duckdb

from stress_dw.evidence import EVIDENCE_DIR, write_rows
from stress_dw.indicators import INDICATORS, run_indicator
from stress_dw.pipeline import SOURCE_PATH, run_pipeline

DATABASE = Path("data/query-time.duckdb")
QUERY_TIME_FILE = "query-time.csv"
QUERY_TIME_HEADER = ("indicator", "runs", "median_ms", "min_ms", "max_ms")
RUNS = 5


def measure(call: Callable[[], object], runs: int = RUNS) -> list[float]:
    """Run `call` once unmeasured, then `runs` times, in milliseconds."""
    call()
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        call()
        times.append((time.perf_counter() - start) * 1000)
    return times


def milliseconds(value: float) -> str:
    """Write a time in milliseconds at one decimal place."""
    return f"{value:.1f}"


def main() -> None:
    """Reload `DATABASE`, time each indicator, and write `query-time.csv`."""
    for stale in (DATABASE, DATABASE.with_name(DATABASE.name + ".wal")):
        stale.unlink(missing_ok=True)
    rows = []
    with duckdb.connect(DATABASE) as connection:
        run_pipeline(connection, SOURCE_PATH)
        for number in INDICATORS:
            times = measure(partial(run_indicator, connection, number))
            rows.append(
                (
                    number,
                    RUNS,
                    milliseconds(statistics.median(times)),
                    milliseconds(min(times)),
                    milliseconds(max(times)),
                )
            )
    write_rows(EVIDENCE_DIR / QUERY_TIME_FILE, QUERY_TIME_HEADER, rows)
    print(
        f"duckdb {duckdb.__version__}; python {platform.python_version()}; "
        f"{platform.platform()}; {platform.machine()}; {os.cpu_count()} logical CPUs"
    )


if __name__ == "__main__":
    main()
