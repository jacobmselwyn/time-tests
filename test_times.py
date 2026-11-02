import pytest

from times import time_range, compute_overlap_time

def test_given_input():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    result = compute_overlap_time(large, short)
    expected = [
        ("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
        ("2010-01-12 10:38:00", "2010-01-12 10:45:00"),
    ]
    assert result == expected


def test_no_overlap():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 12:30:00", "2010-01-12 13:00:00", 2, 60)
    result = compute_overlap_time(large, short)
    expected = []
    assert result == expected

def test_several_intervals_each():
    first = time_range("2010-01-12 10:00:00", "2010-01-12 10:10:00", 2, 60)
    second = time_range("2010-01-12 10:02:00", "2010-01-12 10:12:00", 2, 60)
    result = compute_overlap_time(first, second)
    expected = [
        ("2010-01-12 10:02:00", "2010-01-12 10:04:30"),
        ("2010-01-12 10:05:30", "2010-01-12 10:06:30"),
        ("2010-01-12 10:07:30", "2010-01-12 10:10:00"),
    ]
    assert result == expected

def test_end_same_time_when_other_starts():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 12:00:00", "2010-01-12 13:00:00", 2, 60)
    result = compute_overlap_time(large, short)
    expected = []
    assert result == expected

def test_date_going_backwards():
    with pytest.raises(ValueError):
        time_range(
            "2010-01-12 12:00:00",
            "2010-01-12 10:00:00"
        )
