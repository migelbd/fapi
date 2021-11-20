import urllib.parse
from functools import lru_cache
from typing import Optional
from urllib.parse import urlencode
from pydantic import PostgresDsn

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_env: str = 'development'
    super_user_token: Optional[str]
    app_debug: bool = False
    sentry_dsn: Optional[str]
    postgres_dsn: Optional[PostgresDsn]

    class Config:
        env_file = '.env'

    def db_connection_string(self) -> str:
        if not self.postgres_dsn:
            return 'sqlite://./app.db'
        return self.postgres_dsn


@lru_cache()
def settings():
    return Settings()
