import os
from typing import Generator

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from app.db.models.data import DataFighter, DataMatch
from app import config


SQLALCHEMY_DATABASE_URL = f"mysql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}?charset=utf8"
WAREHOUSE_DATABASE_URL = os.environ.get("AIRFLOW_MYSQL_ALCHEMY")

ware_engine = create_engine(
    WAREHOUSE_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=15,
    max_overflow=0,
    encoding="utf8",
    convert_unicode=True,
)
ware_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ware_engine)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=15,
    max_overflow=0,
    encoding="utf8",
    convert_unicode=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_ware_db() -> Generator:
    """
    호출되면 DB 연결하고 작업 완료되면 close
    """
    db = ware_SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db() -> Generator:
    """
    호출되면 DB 연결하고 작업 완료되면 close
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_ware_table():
    inspector = inspect(ware_engine)
    tables = [DataFighter, DataMatch]

    for table in tables:
        if inspector.has_table(table.__tablename__):
            pass
        else:
            table.__table__.create(ware_engine)
