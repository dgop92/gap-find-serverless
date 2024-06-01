import math
from typing import List, Tuple


def npzeros(rows: int, columns: int) -> List[List[float]]:
    return [[0 for _ in range(columns)] for _ in range(rows)]


def nptranspose(matrix: List[List[float]]) -> List[List[float]]:
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def npfull(rows: int, fill_value: int) -> List[float]:
    return [fill_value for _ in range(rows)]


def npwhere(matrix: List[List[float]], value: float) -> Tuple[List[int], List[int]]:
    rows = len(matrix)
    columns = len(matrix[0])

    row_indices = []
    column_indices = []

    for i in range(rows):
        for j in range(columns):
            if matrix[i][j] == value:
                row_indices.append(i)
                column_indices.append(j)

    return row_indices, column_indices


def npwhere_find_zeros(matrix: List[List[float]]) -> Tuple[List[int], List[int]]:
    return npwhere(matrix, 0)


def npsum(matricies: List[List[List[float]]]) -> List[List[float]]:
    rows = len(matricies[0])
    columns = len(matricies[0][0])
    new_matrix = npzeros(rows, columns)

    for matrix in matricies:
        for i in range(rows):
            for j in range(columns):
                new_matrix[i][j] += matrix[i][j]

    return new_matrix


def npmean(matricies: List[List[List[float]]]) -> List[List[float]]:
    matrix_sum = npsum(matricies)

    rows = len(matricies[0])
    columns = len(matricies[0][0])

    matrix_mean = npzeros(rows, columns)

    n = len(matricies)

    for i in range(rows):
        for j in range(columns):
            matrix_mean[i][j] = matrix_sum[i][j] / n

    return matrix_mean


def npstd(matricies: List[List[List[float]]]) -> List[List[float]]:
    matrix_mean = npmean(matricies)

    rows = len(matricies[0])
    columns = len(matricies[0][0])

    matrix_std = npzeros(rows, columns)

    new_matricies = []
    for matrix in matricies:
        new_matrix = npzeros(rows, columns)
        for i in range(rows):
            for j in range(columns):
                new_matrix[i][j] = (matrix[i][j] - matrix_mean[i][j]) ** 2
        new_matricies.append(new_matrix)

    matrix_sum = npsum(new_matricies)

    n = len(matricies)

    for i in range(rows):
        for j in range(columns):
            matrix_std[i][j] = math.sqrt(matrix_sum[i][j] / n)

    return matrix_std
