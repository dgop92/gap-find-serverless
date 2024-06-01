from typing import List, Tuple

from core.analyze_meetings import get_schedule_meeting_data
from core.db import UsernameDB
from core.entities import AnalyzeMeetingInput, AnalyzeMeetingResult
from core.responses import BadRequestResponse, BadRequestResponseException


def get_schedules(usernames: List[str], repository: UsernameDB) -> List[str]:
    schedules = repository.get_multiple_user_schedule(usernames)
    username_schedule = zip(usernames, schedules)
    usernames_without_schedule = [
        username for username, schedule in username_schedule if not schedule
    ]

    if len(usernames) - len(usernames_without_schedule) < 2:
        response = BadRequestResponse(
            body={
                "usernames": [
                    f"Los siguientes usuarios no se encontraron: {','.join(usernames_without_schedule)}. Hay menos de 2 usuarios, por ende no se puede realizar un análisis."
                ]
            },
        )
        raise BadRequestResponseException(response)

    users_with_schedule = [schedule for schedule in schedules if schedule]
    return users_with_schedule


def get_meeting_analysis(
    input_data: AnalyzeMeetingInput, repository: UsernameDB
) -> Tuple[int, List[AnalyzeMeetingResult]]:
    string_schedules = get_schedules(input_data.usernames, repository)

    ss_to_filter: str | None = None
    if input_data.username_to_filter is not None:
        ss_to_filter = repository.get_user_schedule(input_data.username_to_filter)
        if ss_to_filter is None:
            raise BadRequestResponseException(
                BadRequestResponse(
                    body={
                        "username_to_filter": [
                            f"El usuario {input_data.username_to_filter} no se encontró"
                        ]
                    }
                )
            )

    result = get_schedule_meeting_data(string_schedules, ss_to_filter)

    meeting_results = [
        AnalyzeMeetingResult(
            day_index=r["day_index"],
            hour_index=r["hour_index"],
            number_of_students=r["number_of_students"],
            availability=r["availability"],
        )
        for r in result["results"]
    ]

    return len(string_schedules), meeting_results
