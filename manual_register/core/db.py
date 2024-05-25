from typing import Protocol

import redis


class UsernameDB(Protocol):

    def save_user(self, username: str, schedule: str) -> None: ...


class UsernameMockDB:

    def __init__(self) -> None:
        self.data = {}

    def save_user(self, username: str, schedule: str) -> None:
        self.data[username] = schedule


class UsernameRedisDB:

    def __init__(self, url: str) -> None:
        self.redis = redis.Redis.from_url(url)

    def save_user(self, username: str, schedule: str) -> None:
        self.redis.set(f"gapfind:{username}", schedule)
