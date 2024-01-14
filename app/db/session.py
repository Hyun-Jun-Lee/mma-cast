import os
from typing import Generator

from pymongo import MongoClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from app.db.models.data import DataFighter, DataMatch
from app import config


SQLALCHEMY_DATABASE_URL = f"mysql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}?charset=utf8"
MONGODB_DATABASE_URL = f"mongodb+srv://{config.RAW_DB_USER}:{config.RAW_DB_PASSWORD}@{config.CLUSTER_NAME}.7bddfbe.mongodb.net/{config.RAW_DB_NAME}?retryWrites=true&w=majority"

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
def get_raw_db():
    """
    호출되면 MongoDB 연결하고 작업 완료되면 close
    """
    client = MongoClient(MONGODB_DATABASE_URL)
    db = client.get_default_database()  # 기본 데이터베이스 사용, 또는 명시적으로 데이터베이스 이름 지정 가능
    try:
        yield db
    finally:
        client.close()


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
