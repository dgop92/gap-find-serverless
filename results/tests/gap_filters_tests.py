import unittest

from core.gap_filters import (
    filter_by_days,
    limit_results,
    sort_results,
    sort_results_by_quality,
)

assertions = unittest.TestCase()


def test_sort_results():

    # testing, not all the values in gap item are included
    test_gaps = [
        {
            "avg": 1.5,
            "sd": 1.0,
            "day_index": 0,
            "hour_index": 6,
        },
        {
            "avg": 2.5,
            "sd": 2.0,
            "day_index": 2,
            "hour_index": 3,
        },
        {
            "avg": 1.0,
            "sd": 0.5,
            "day_index": 1,
            "hour_index": 1,
        },
    ]

    results = sort_results(test_gaps, with_sd=False)
    assertions.assertListEqual(list(map(lambda e: e["day_index"], results)), [1, 0, 2])


def test_sort_by_quality():

    test_gaps = [
        {
            "quality": 0.756,
            "day_index": 0,
            "hour_index": 6,
        },
        {
            "quality": 0.463,
            "day_index": 2,
            "hour_index": 3,
        },
        {
            "quality": 0.986,
            "day_index": 1,
            "hour_index": 1,
        },
    ]

    # quality computed by avgerage
    results = sort_results_by_quality(test_gaps)
    assertions.assertListEqual(list(map(lambda e: e["day_index"], results)), [1, 0, 2])


def test_sort_results_with_sd():

    test_gaps = [
        {
            "avg": 1.0,
            "sd": 1.5,
            "day_index": 0,
            "hour_index": 6,
        },
        {
            "avg": 2.5,
            "sd": 2.0,
            "day_index": 2,
            "hour_index": 3,
        },
        {
            "avg": 1.0,
            "sd": 2.0,
            "day_index": 1,
            "hour_index": 1,
        },
    ]

    results = sort_results(test_gaps, with_sd=True)
    assertions.assertListEqual(list(map(lambda e: e["day_index"], results)), [0, 1, 2])


def test_limit_results():

    test_gaps = [
        {
            "day_index": 0,
            "hour_index": 6,
        },
        {
            "day_index": 2,
            "hour_index": 3,
        },
        {
            "day_index": 1,
            "hour_index": 1,
        },
    ]

    results = limit_results(test_gaps, limit=-1)
    assertions.assertListEqual(list(map(lambda e: e["day_index"], results)), [0, 2, 1])
    results = limit_results(test_gaps, limit=1)
    assertions.assertListEqual(list(map(lambda e: e["day_index"], results)), [0])


def test_filter_by_days():

    test_gaps = [
        {
            "day_index": 0,
            "hour_index": 6,
        },
        {
            "day_index": 2,
            "hour_index": 3,
        },
        {
            "day_index": 1,
            "hour_index": 11,
        },
        {
            "day_index": 1,
            "hour_index": 12,
        },
    ]

    results = filter_by_days(test_gaps, day_indices=[1, 0])
    filtered_results = set(map(lambda e: e["hour_index"], results))
    assertions.assertSetEqual(filtered_results, set([3]))

    results = filter_by_days(test_gaps, day_indices=[2])
    filtered_results = set(map(lambda e: e["hour_index"], results))
    assertions.assertSetEqual(filtered_results, set([11, 12, 6]))
