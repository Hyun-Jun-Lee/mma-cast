from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings, Settings

config: Settings = get_settings()

SQLALCHEMY_DATABASE_URL = f"mysql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=15,
    max_overflow=0,
    encoding="utf8",
    convert_unicode=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    호출되면 DB 연결하고 작업 완료되면 close
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
