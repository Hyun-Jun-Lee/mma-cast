from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    CORS_ORIGINS: str
    TOKEN_EXPIRE_MINUTE: int
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
