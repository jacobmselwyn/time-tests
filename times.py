import datetime

import requests


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, TIME_FORMAT)
    end_time_s = datetime.datetime.strptime(end_time, TIME_FORMAT)
    if end_time_s < start_time_s:
        raise ValueError("End time cannot be before start time")
    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1)
    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                  start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                 for i in range(number_of_intervals)]
    return [(ta.strftime(TIME_FORMAT), tb.strftime(TIME_FORMAT)) for ta, tb in sec_range]


def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            low = max(start1, start2)
            high = min(end1, end2)
            if low < high:
                overlap_time.append((low, high))
    return overlap_time


def iss_passes(latitude, longitude, api_key, altitude=0, days=5, min_visibility=50):
    """Return visible ISS passes as (start, end) pairs of UTC time strings."""
    url = (
        "https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/"
        f"{latitude}/{longitude}/{altitude}/{days}/{min_visibility}/&apiKey={api_key}"
    )
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    intervals = []
    for iss_pass in response.json()["passes"]:
        start = datetime.datetime.fromtimestamp(iss_pass["startUTC"], datetime.timezone.utc)
        end = datetime.datetime.fromtimestamp(iss_pass["endUTC"], datetime.timezone.utc)
        intervals.append((start.strftime(TIME_FORMAT), end.strftime(TIME_FORMAT)))
    return intervals
