from typing import List, Tuple

from core.constants import DAYS_PER_WEEK


def find_ss_from_class_hours(list_of_indices: List[Tuple[int, int]]):
    ss_list = [0 for _ in range(98)]
    for day_hour in list_of_indices:
        hour_index, day_index = day_hour
        pos = hour_index * DAYS_PER_WEEK + day_index
        ss_list[pos] = 1
    string_schedule = "".join(map(str, ss_list))
    return string_schedule
