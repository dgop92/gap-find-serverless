from typing import Any, Dict, List, Protocol

import redis


class UsernameDB(Protocol):

    def get_user_schedule(self, username: str) -> str | None: ...

    def get_multiple_user_schedule(self, usernames: list[str]) -> List[str | None]: ...


class UsernameMockDB:

    def __init__(self) -> None:
        self.data: Dict[str, str] = {}

    def get_user_schedule(self, username: str) -> str | None:
        return self.data.get(username, None)

    def get_multiple_user_schedule(self, usernames: list[str]) -> List[str | None]:
        return [self.get_user_schedule(username) for username in usernames]


class UsernameRedisDB:

    def __init__(self, url: str) -> None:
        self.redis = redis.Redis.from_url(url)

    def get_user_schedule(self, username: str) -> str | None:
        response: Any = self.redis.get(f"gapfind:{username}")
        schedule = response.decode("utf-8") if response else None
        return schedule

    def get_multiple_user_schedule(self, usernames: list[str]) -> List[str | None]:
        responses: Any = self.redis.mget(
            [f"gapfind:{username}" for username in usernames]
        )
        schedules = [
            response.decode("utf-8") if response else None for response in responses
        ]
        return schedules
