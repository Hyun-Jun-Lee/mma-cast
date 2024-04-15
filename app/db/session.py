import os
from typing import Generator
from urllib.parse import quote_plus

from pymongo import MongoClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from app import config

MONGODB_DATABASE_URL = f"mongodb://{config.MONGO_INITDB_ROOT_USERNAME}:{config.MONGO_INITDB_ROOT_PASSWORD}@mongodb:27017"


@contextmanager
def get_mongo_db():
    """
    호출되면 MongoDB 연결하고 작업 완료되면 close
    """
    client = MongoClient(MONGODB_DATABASE_URL)
    db = client[config.MONGODB_NAME]
    try:
        yield db
    finally:
        client.close()


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=15,
    max_overflow=0,
    encoding="utf8",
    convert_unicode=True,
)
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


@contextmanager
def get_ps_db() -> Generator:
    """
    호출되면 DB 연결하고 작업 완료되면 close
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
