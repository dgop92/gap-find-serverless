import unittest

from core.schedule_logic import find_ss_from_class_hours

assertions = unittest.TestCase()


def test_find_ss_from_class_hours():

    expected_ss = "01000000100100001010001000000000000000000000000000000000011010001101001010000111000000000000000000"

    list_of_indicies = [
        (0, 1),
        (1, 1),
        (1, 4),
        (2, 2),
        (2, 4),
        (3, 1),
        (8, 1),
        (8, 2),
        (8, 4),
        (9, 1),
        (9, 2),
        (9, 4),
        (10, 0),
        (10, 2),
        (11, 0),
        (11, 1),
        (11, 2),
    ]

    string_schedule = find_ss_from_class_hours(list_of_indicies)
    assertions.assertEqual(string_schedule, expected_ss)
