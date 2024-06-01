import unittest

from core.distance_algorithms import (
    apply_distance_to_bit_matrix,
    from_string_to_bit_matrix,
    indices_of_sub_arrays_of_zeros,
    put_distance_to_day,
)

string_schedule1 = "01000000100100001010001000000000000000000000000000000000011010001101001010000111000000000000000000"
string_schedule2 = "01000000111100011100001010000001000000000000100000010000010100011010001100000000100000000000000000"

assertions = unittest.TestCase()


def test_indices_of_sub_arrays_of_zeros():

    arr = [0, 0, 0, 1, 1, 1, 0, 1, 0]
    indices = list(indices_of_sub_arrays_of_zeros(arr))
    assertions.assertListEqual(indices, [(0, 3), (6, 7), (8, 9)])

    arr = [0, 1, 0, 1, 1, 1]
    indices = list(indices_of_sub_arrays_of_zeros(arr))
    assertions.assertListEqual(indices, [(0, 1), (2, 3)])

    arr = [0, 1, 1, 1, 1, 1]
    indices = list(indices_of_sub_arrays_of_zeros(arr))
    assertions.assertNotEqual(indices, [(0, 1), (2, 3)])


def test_put_distance_to_day():

    arr = [0, 0, 0, 1, 1, 1, 0, 1, 0]
    put_distance_to_day(0, 3, arr)
    assertions.assertListEqual(arr, [3, 2, 1, 1, 1, 1, 0, 1, 0])

    arr = [0, 0, 1, 1, 0, 1, 1, 0, 0]
    indices = list(indices_of_sub_arrays_of_zeros(arr))
    for gap in indices:
        put_distance_to_day(*gap, arr)
    assertions.assertListEqual(arr, [2, 1, 0, 0, 1, 0, 0, 1, 2])


def test_from_string_to_bit_matrix():

    bit_matrix = from_string_to_bit_matrix(string_schedule1)
    expected_matrix = [
        [0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [1, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]

    assertions.assertListEqual(bit_matrix, expected_matrix)

    bit_matrix = from_string_to_bit_matrix(string_schedule2)
    expected_matrix = [
        [0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [1, 1, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]

    assertions.assertListEqual(bit_matrix, expected_matrix)


def test_apply_distance_to_bit_matrix():

    bit_matrix = from_string_to_bit_matrix(string_schedule1)
    apply_distance_to_bit_matrix(bit_matrix)
    expected_matrix = [
        [10, 0, 2, 0, 1, 0, 0],
        [9, 0, 1, 0, 0, 0, 0],
        [8, 1, 0, 0, 0, 0, 0],
        [7, 0, 1, 0, 1, 0, 0],
        [6, 1, 2, 0, 2, 0, 0],
        [5, 2, 3, 0, 3, 0, 0],
        [4, 2, 2, 0, 2, 0, 0],
        [3, 1, 1, 0, 1, 0, 0],
        [2, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 2, 0, 0],
        [1, 1, 1, 0, 3, 0, 0],
        [2, 2, 2, 0, 4, 0, 0],
    ]

    assertions.assertListEqual(bit_matrix, expected_matrix)

    bit_matrix = from_string_to_bit_matrix(string_schedule2)
    apply_distance_to_bit_matrix(bit_matrix)
    expected_matrix = [
        [9, 0, 1, 1, 1, 0, 0],
        [8, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 1, 0, 0],
        [6, 0, 1, 0, 2, 0, 0],
        [5, 1, 2, 0, 3, 0, 0],
        [4, 2, 1, 1, 4, 0, 0],
        [3, 2, 0, 2, 5, 0, 0],
        [2, 1, 0, 1, 6, 0, 0],
        [1, 0, 1, 0, 7, 0, 0],
        [0, 0, 2, 0, 8, 0, 0],
        [0, 0, 3, 1, 9, 0, 0],
        [1, 1, 4, 0, 10, 0, 0],
        [2, 2, 5, 1, 11, 0, 0],
        [3, 3, 6, 2, 12, 0, 0],
    ]

    assertions.assertListEqual(bit_matrix, expected_matrix)
