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
    CELERY_NAME: str
    CELERY_POOL: str
    CELERY_CONCURRENCY: str
    RABBITMQ_USER: str
    RABBITMQ_PW: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACK: str
    AIRFLOW_UID: int
    WAREHOUSE_DB: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
