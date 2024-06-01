from core.constants import DAYS_PER_WEEK, HOURS_PER_DAY
from core.distance_algorithms import from_string_to_bit_matrix
from core.np_utilities import npsum


def is_needed_to_ignore_hour(filter_schedule, i, j):
    if filter_schedule:
        pos = i * DAYS_PER_WEEK + j
        return bool(int(filter_schedule[pos]))

    return False


def get_sum_meeting_matrix(string_schedules):
    bit_matrices = list(map(from_string_to_bit_matrix, string_schedules))
    return npsum(bit_matrices)


def filter_results(result, filter_schedule):

    i = result["hour_index"]
    j = result["day_index"]

    if j > 4:
        return False

    return not is_needed_to_ignore_hour(filter_schedule, i, j)


def get_schedule_meeting_data(string_schedules, filter_schedule=None):
    sum_matrix = get_sum_meeting_matrix(string_schedules)
    total_students = len(string_schedules)
    hours, days = HOURS_PER_DAY, DAYS_PER_WEEK
    results = []
    for i in range(hours):
        for j in range(days):

            # the number of students available at this time
            number_of_students = total_students - sum_matrix[i][j]
            availability = number_of_students / total_students
            results.append(
                {
                    "day_index": j,
                    "hour_index": i,
                    "number_of_students": number_of_students,
                    "availability": availability,
                }
            )

    filtered_results = list(
        filter(lambda result: filter_results(result, filter_schedule), results)
    )

    return {"total_students": total_students, "results": filtered_results}
