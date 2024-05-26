import unittest

from core.distance_algorithms import get_distance_matrix_from_string_schedule
from core.finder import DistanceMatrixComputer

string_schedule1 = "01000000100100001010001000000000000000000000000000000000011010001101001010000111000000000000000000"
string_schedule2 = "01000000111100011100001010000001000000000000100000010000010100011010001100000000100000000000000000"


class TestMatrixComputer(unittest.TestCase):
    def test_set_to_one_no_classes_days_default_options(self):
        distance_matrix = get_distance_matrix_from_string_schedule(string_schedule1)
        dc = DistanceMatrixComputer([distance_matrix])
        dc.set_to_one_no_classes_days()

        expected_matrix = [
            [10, 0, 2, 1, 1, 0, 0],
            [9, 0, 1, 1, 0, 0, 0],
            [8, 1, 0, 1, 0, 0, 0],
            [7, 0, 1, 1, 1, 0, 0],
            [6, 1, 2, 1, 2, 0, 0],
            [5, 2, 3, 1, 3, 0, 0],
            [4, 2, 2, 1, 2, 0, 0],
            [3, 1, 1, 1, 1, 0, 0],
            [2, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 1, 0, 0],
            [0, 0, 0, 1, 2, 0, 0],
            [1, 1, 1, 1, 3, 0, 0],
            [2, 2, 2, 1, 4, 0, 0],
        ]

        self.assertListEqual(dc.distance_matrices[0], expected_matrix)

    def test_set_to_one_no_classes_days_with_weekends(self):
        distance_matrix = get_distance_matrix_from_string_schedule(string_schedule1)
        dc = DistanceMatrixComputer(
            [distance_matrix], options={"ignore_weekend": False}
        )
        dc.set_to_one_no_classes_days()

        expected_matrix = [
            [10, 0, 2, 1, 1, 1, 1],
            [9, 0, 1, 1, 0, 1, 1],
            [8, 1, 0, 1, 0, 1, 1],
            [7, 0, 1, 1, 1, 1, 1],
            [6, 1, 2, 1, 2, 1, 1],
            [5, 2, 3, 1, 3, 1, 1],
            [4, 2, 2, 1, 2, 1, 1],
            [3, 1, 1, 1, 1, 1, 1],
            [2, 0, 0, 1, 0, 1, 1],
            [1, 0, 0, 1, 0, 1, 1],
            [0, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 2, 1, 1],
            [1, 1, 1, 1, 3, 1, 1],
            [2, 2, 2, 1, 4, 1, 1],
        ]

        self.assertListEqual(dc.distance_matrices[0], expected_matrix)

    def test_zerofication_of_matrices(self):
        distance_matrices = list(
            map(
                get_distance_matrix_from_string_schedule,
                [string_schedule1, string_schedule2],
            )
        )

        dc = DistanceMatrixComputer(distance_matrices)
        dc.zerofication_of_matrices()

        first_matrix = [
            [10, 0, 2, 0, 1, 0, 0],
            [9, 0, 0, 0, 0, 0, 0],
            [8, 0, 0, 0, 0, 0, 0],
            [7, 0, 1, 0, 1, 0, 0],
            [6, 1, 2, 0, 2, 0, 0],
            [5, 2, 3, 0, 3, 0, 0],
            [4, 2, 0, 0, 2, 0, 0],
            [3, 1, 0, 0, 1, 0, 0],
            [2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 2, 0, 0],
            [1, 1, 1, 0, 3, 0, 0],
            [2, 2, 2, 0, 4, 0, 0],
        ]

        second_matrix = [
            [9, 0, 1, 0, 1, 0, 0],
            [8, 0, 0, 0, 0, 0, 0],
            [7, 0, 0, 0, 0, 0, 0],
            [6, 0, 1, 0, 2, 0, 0],
            [5, 1, 2, 0, 3, 0, 0],
            [4, 2, 1, 0, 4, 0, 0],
            [3, 2, 0, 0, 5, 0, 0],
            [2, 1, 0, 0, 6, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 9, 0, 0],
            [0, 0, 0, 0, 10, 0, 0],
            [2, 2, 5, 0, 11, 0, 0],
            [3, 3, 6, 0, 12, 0, 0],
        ]

        self.assertListEqual(dc.distance_matrices[0], first_matrix)
        self.assertListEqual(dc.distance_matrices[1], second_matrix)

    def test_sum_matrix_with_default_options(self):
        distance_matrices = list(
            map(
                get_distance_matrix_from_string_schedule,
                [string_schedule1, string_schedule2],
            )
        )

        dc = DistanceMatrixComputer(distance_matrices)
        dc.compute()

        expected_matrix = [
            [19, 0, 3, 0, 2, 0, 0],
            [17, 0, 0, 0, 0, 0, 0],
            [15, 0, 0, 0, 0, 0, 0],
            [13, 0, 2, 0, 3, 0, 0],
            [11, 2, 4, 0, 5, 0, 0],
            [9, 4, 4, 0, 7, 0, 0],
            [7, 4, 0, 0, 7, 0, 0],
            [5, 2, 0, 0, 7, 0, 0],
            [3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 10, 0, 0],
            [0, 0, 0, 0, 12, 0, 0],
            [3, 3, 6, 0, 14, 0, 0],
            [5, 5, 8, 0, 16, 0, 0],
        ]

        sum_matrix = dc.get_sum_matrix()
        self.assertIsNotNone(sum_matrix)
        self.assertListEqual(sum_matrix, expected_matrix)  # type: ignore

    def test_avg_matrix_with_default_options(self):
        distance_matrices = list(
            map(
                get_distance_matrix_from_string_schedule,
                [string_schedule1, string_schedule2],
            )
        )

        dc = DistanceMatrixComputer(distance_matrices)
        dc.compute()

        expected_matrix = [
            [9.5, 0.0, 1.5, 0.0, 1.0, 0.0, 0.0],
            [8.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [7.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [6.5, 0.0, 1.0, 0.0, 1.5, 0.0, 0.0],
            [5.5, 1.0, 2.0, 0.0, 2.5, 0.0, 0.0],
            [4.5, 2.0, 2.0, 0.0, 3.5, 0.0, 0.0],
            [3.5, 2.0, 0.0, 0.0, 3.5, 0.0, 0.0],
            [2.5, 1.0, 0.0, 0.0, 3.5, 0.0, 0.0],
            [1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 6.0, 0.0, 0.0],
            [1.5, 1.5, 3.0, 0.0, 7.0, 0.0, 0.0],
            [2.5, 2.5, 4.0, 0.0, 8.0, 0.0, 0.0],
        ]

        matrix_mean = dc.get_avg_matrix()
        self.assertIsNotNone(matrix_mean)

        for i, row in enumerate(matrix_mean):  # type: ignore
            for j, value in enumerate(row):
                self.assertAlmostEqual(value, expected_matrix[i][j])

    def test_sd_matrix(self):

        distance_matrices = list(
            map(
                get_distance_matrix_from_string_schedule,
                [string_schedule1, string_schedule2],
            )
        )

        expected_matrix = [
            [0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0],
            [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0],
            [0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0],
            [0.5, 0.0, 1.0, 0.0, 0.5, 0.0, 0.0],
            [0.5, 0.0, 0.0, 0.0, 1.5, 0.0, 0.0],
            [0.5, 0.0, 0.0, 0.0, 2.5, 0.0, 0.0],
            [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 4.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 4.0, 0.0, 0.0],
            [0.5, 0.5, 2.0, 0.0, 4.0, 0.0, 0.0],
            [0.5, 0.5, 2.0, 0.0, 4.0, 0.0, 0.0],
        ]

        dc = DistanceMatrixComputer(distance_matrices, options={"compute_sd": True})
        dc.compute()

        matrix_sd = dc.get_sd_matrix()
        self.assertIsNotNone(matrix_sd)

        for i, row in enumerate(matrix_sd):  # type: ignore
            for j, value in enumerate(row):
                self.assertAlmostEqual(value, expected_matrix[i][j])
