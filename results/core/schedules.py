from typing import List

from core.db import UsernameDB
from core.responses import BadRequestResponse, GenericJSONResponse


def get_schedules(
    usernames: List[str], repository: UsernameDB
) -> List[str] | GenericJSONResponse:
    schedules = repository.get_multiple_user_schedule(usernames)
    username_schedule = zip(usernames, schedules)
    usernames_without_schedule = [
        username for username, schedule in username_schedule if not schedule
    ]
    if len(usernames_without_schedule) > 0:
        return BadRequestResponse(
            body={
                "usernames": [
                    f"Los siguientes usuarios no se encontraron {','.join(usernames_without_schedule)}:"
                ]
            },
        )
    users_with_schedule = [schedule for schedule in schedules if schedule]
    return users_with_schedule
