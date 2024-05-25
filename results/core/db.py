from typing import Any, Dict, Protocol

import redis


class UsernameDB(Protocol):

    def get_user_schedule(self, username: str) -> str | None: ...


class UsernameMockDB:

    def __init__(self) -> None:
        self.data: Dict[str, str] = {}

    def get_user_schedule(self, username: str) -> str | None:
        return self.data.get(username, None)


class UsernameRedisDB:

    def __init__(self, url: str) -> None:
        self.redis = redis.Redis.from_url(url)

    def get_user_schedule(self, username: str) -> str | None:
        response: Any = self.redis.get(username)
        schedule = response.decode("utf-8") if response else None
        return schedule
