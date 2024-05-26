from typing import List

from core.db import UsernameDB
from core.distance_algorithms import get_distance_matrix_from_string_schedule
from core.entities import GapItem, ResultsInput
from core.finder import DistanceMatrixComputer, GapFinder
from core.gap_filters import filter_by_days, limit_results
from core.responses import BadRequestResponse, BadRequestResponseException


def get_schedules(usernames: List[str], repository: UsernameDB) -> List[str]:
    schedules = repository.get_multiple_user_schedule(usernames)
    username_schedule = zip(usernames, schedules)
    usernames_without_schedule = [
        username for username, schedule in username_schedule if not schedule
    ]
    if len(usernames_without_schedule) > 0:
        response = BadRequestResponse(
            body={
                "usernames": [
                    f"Los siguientes usuarios no se encontraron {','.join(usernames_without_schedule)}:"
                ]
            },
        )
        raise BadRequestResponseException(response)

    users_with_schedule = [schedule for schedule in schedules if schedule]
    return users_with_schedule


def get_gaps(input_data: ResultsInput, repository: UsernameDB) -> List[GapItem]:

    string_schedules = get_schedules(input_data.usernames, repository)
    distance_matrices = list(
        map(get_distance_matrix_from_string_schedule, string_schedules)
    )
    distance_matrix_computer = DistanceMatrixComputer(
        distance_matrices,
        options={
            "compute_sd": input_data.compute_sd,
            "no_classes_day": input_data.no_classes_day,
            "ignore_weekend": input_data.ignore_weekend,
        },
    )
    gap_finder = GapFinder(distance_matrix_computer)
    gap_finder.find_gaps()

    if input_data.days_to_filter is not None:
        gap_finder.apply_filter(filter_by_days, input_data.days_to_filter)
    if input_data.limit is not None:
        gap_finder.apply_filter(limit_results, input_data.limit)

    gaps = gap_finder.get_results()

    gap_items = [
        GapItem(
            day=gap["day"],
            hour=gap["hour"],
            avg=gap["avg"],
            quality=gap["quality"],
            day_index=gap["day_index"],
            hour_index=gap["hour_index"],
            sd=gap.get("sd", None),
        )
        for gap in gaps
    ]
    return gap_items
