from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from times import compute_overlap_time, iss_passes, time_range

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


def test_iss_passes():
    with patch("times.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "passes": [
                {"startUTC": 1704067200, "endUTC": 1704067500},
                {"startUTC": 1704073200, "endUTC": 1704073440},
            ]
        }

        result = iss_passes(56, 0, "test-key")

    mock_get.assert_called_once_with(
        "https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/56/0/0/5/50/"
        "&apiKey=test-key",
        timeout=10,
    )
    assert result == [
        ("2024-01-01 00:00:00", "2024-01-01 00:05:00"),
        ("2024-01-01 01:40:00", "2024-01-01 01:44:00"),
    ]
