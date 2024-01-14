import os

CORS_ORIGINS = os.environ.get("CORS_ORIGINS")
TOKEN_EXPIRE_MINUTE = os.environ.get("TOKEN_EXPIRE_MINUTE")

# db
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

# mongodb
RAW_DB_USER = os.environ.get("RAW_DB_USER")
RAW_DB_PASSWORD = os.environ.get("RAW_DB_PASSWORD")
RAW_DB_NAME = os.environ.get("RAW_DB_NAME")
CLUSTER_NAME = os.environ.get("CLUSTER_NAME")

# celery
CELERY_NAME = os.environ.get("CELERY_NAME")
CELERY_POOL = os.environ.get("CELERY_POOL")
CELERY_CONCURRENCY = os.environ.get("CELERY_CONCURRENCY")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER")
RABBITMQ_PW = os.environ.get("RABBITMQ_PW")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
