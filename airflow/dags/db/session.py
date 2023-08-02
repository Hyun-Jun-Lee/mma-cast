from typing import Generator
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from db.models import DataFighter, DataMatch
from contextlib import contextmanager

# SQLALCHEMY_DATABASE_URL = f"mysql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.WAREHOUSE_DB}?charset=utf8"

SQLALCHEMY_DATABASE_URL = os.environ.get("AIRFLOW_MYSQL_ALCHEMY")


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=15,
    max_overflow=0,
    encoding="utf8",
    convert_unicode=True,
)


def create_table():
    inspector = inspect(engine)
    tables = [DataFighter, DataMatch]

    for table in tables:
        if inspector.has_table(table.__tablename__):
            pass
        else:
            table.__table__.create(engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db() -> Generator:
    """
    호출되면 DB 연결하고 작업 완료되면 close
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
