from pathlib import Path

import pytest
import yaml

from times import time_range, compute_overlap_time

with Path(__file__).with_name("fixture.yaml").open(encoding="utf-8") as fixture_file:
    overlap_cases = yaml.safe_load(fixture_file)


@pytest.mark.parametrize(
    "first_args, second_args, expected",
    [
        pytest.param(
            case["time_range_1"], case["time_range_2"], case["expected"], id=name
        )
        for name, case in overlap_cases.items()
    ],
)
def test_overlap(first_args, second_args, expected):
    first = time_range(*first_args)
    second = time_range(*second_args)
    expected_intervals = [tuple(interval) for interval in expected]
    assert compute_overlap_time(first, second) == expected_intervals


def test_date_going_backwards():
    with pytest.raises(ValueError):
        time_range(
            "2010-01-12 12:00:00",
            "2010-01-12 10:00:00"
        )
