from core.constants import AVG_BOUNDRIES, DAYS, HOURS, HOURS_PER_DAY, SD_BOUNDRIES
from core.gap_filters import sort_results_by_quality
from core.np_utilities import (
    npfull,
    npmean,
    npstd,
    npsum,
    nptranspose,
    npwhere_find_zeros,
)

DEFAULT_MATRIX_COMPUTER_OPTIONS = {
    "compute_sd": False,
    "no_classes_day": False,
    "ignore_weekend": True,
}


class DistanceMatrixComputer:
    """
    Compute sum, average and standard deviation of all distances matrices

    """

    def __init__(self, distance_matrices, options=None):
        self.distance_matrices = distance_matrices
        self.sum_matrix = None
        self.avg_matrix = None
        self.deviation_matrix = None

        self.set_options(options)

    def set_options(self, options=None):
        if options:
            self.options = {**DEFAULT_MATRIX_COMPUTER_OPTIONS, **options}
        else:
            self.options = DEFAULT_MATRIX_COMPUTER_OPTIONS

    def compute(self):
        if self.options["no_classes_day"]:
            self.set_to_one_no_classes_days()

        self.zerofication_of_matrices()

        self.sum_matrix = npsum(self.distance_matrices)
        self.avg_matrix = npmean(self.distance_matrices)

        if self.options["compute_sd"]:
            self.deviation_matrix = npstd(self.distance_matrices)

    def zerofication_of_matrices(self):
        zero_indices = set()
        for distance_matrix in self.distance_matrices:
            current_zero_indices = npwhere_find_zeros(distance_matrix)
            n = len(current_zero_indices[0])
            for i in range(n):
                zero_indices.add(
                    (current_zero_indices[0][i], current_zero_indices[1][i])
                )

        for distance_matrix in self.distance_matrices:
            for index_tuple in zero_indices:
                distance_matrix[index_tuple[0]][index_tuple[1]] = 0

    def set_to_one_no_classes_days(self):

        for distance_matrix in self.distance_matrices:
            transpose_matrix = nptranspose(distance_matrix)
            for i, day in enumerate(transpose_matrix):
                if self.options["ignore_weekend"] and i > 4:
                    break

                has_no_classes = not any(day)
                if has_no_classes:
                    transpose_matrix[i] = npfull(
                        HOURS_PER_DAY,
                        1,
                    )

            # as we are not using numpy we must recopy the content manually
            retranspose_bit_matrix = nptranspose(transpose_matrix)
            for i, hour in enumerate(retranspose_bit_matrix):
                distance_matrix[i] = hour

    def get_sum_matrix(self):
        return self.sum_matrix

    def get_avg_matrix(self):
        return self.avg_matrix

    def get_sd_matrix(self):
        return self.deviation_matrix


def get_gap_quality_average(avg, min_avg, max_avg):
    # start from 0
    max_avg -= min_avg
    avg -= min_avg

    return 1 - (avg / max_avg)


def get_gap_quality(avg, sd, min_avg, max_avg, min_sd, max_sd):
    # start from 0
    max_avg -= min_avg
    avg -= min_avg
    max_sd -= min_sd
    sd -= min_sd

    return 1 - ((avg + sd) / (max_avg + max_sd))


class GapFinder:
    """
    Find all gaps from a series of string schedules

    """

    def __init__(self, distance_matrix_computer):
        self.distance_matrix_computer = distance_matrix_computer
        self.distance_matrix_computer.compute()
        self.results = []

        self.compute_sd = self.distance_matrix_computer.options["compute_sd"]

    def find_gaps(self):

        avg_matrix = self.distance_matrix_computer.get_avg_matrix()
        sd_matrix = self.distance_matrix_computer.get_sd_matrix()

        for i, hour in enumerate(HOURS):
            for j, day in enumerate(DAYS):
                if avg_matrix[i][j] != 0:

                    avg = float(avg_matrix[i][j])

                    new_gap_item = {
                        "day": day,
                        "hour": hour,
                        "avg": avg,
                        "quality": get_gap_quality_average(avg, *AVG_BOUNDRIES),
                        "day_index": j,
                        "hour_index": i,
                    }

                    if sd_matrix is not None:
                        sd = float(sd_matrix[i][j])
                        new_gap_item.update(
                            {
                                "sd": sd,
                                "quality": get_gap_quality(
                                    avg, sd, *AVG_BOUNDRIES, *SD_BOUNDRIES
                                ),
                            }
                        )

                    self.results.append(new_gap_item)

        self.results = sort_results_by_quality(self.results)

    def apply_filter(self, func, *args, **kwargs):
        self.results = func(self.results, *args, **kwargs)

    def get_results(self):
        return self.results
