from app.config import (
    CELERY_CONCURRENCY,
    CELERY_NAME,
    CELERY_POOL,
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
)
from celery import Celery

app = Celery(CELERY_NAME, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
