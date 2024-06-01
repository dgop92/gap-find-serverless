from dataclasses import dataclass

from core.config import APP_CONFIG
from core.db import UsernameDB, UsernameMockDB, UsernameRedisDB


@dataclass
class CoreComponents:
    repository: UsernameDB


def core_factory():
    if APP_CONFIG.mock_repository:
        return CoreComponents(repository=UsernameMockDB())
    else:
        return CoreComponents(repository=UsernameRedisDB(url=APP_CONFIG.redis_url))
