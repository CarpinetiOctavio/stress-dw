from stress_dw.query_time import measure, milliseconds


def test_a_measurement_discards_one_warm_up_run() -> None:
    calls: list[int] = []
    times = measure(lambda: calls.append(1), runs=3)
    assert len(calls) == 4
    assert len(times) == 3
    assert all(t >= 0 for t in times)


def test_times_are_written_at_one_decimal_place() -> None:
    assert milliseconds(6.54) == "6.5"
    assert milliseconds(10.0) == "10.0"
