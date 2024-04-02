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
def get_db():
    """
    호출되면 MongoDB 연결하고 작업 완료되면 close
    """
    client = MongoClient(MONGODB_DATABASE_URL)
    db = client[config.MONGODB_NAME]
    try:
        yield db
    finally:
        client.close()
