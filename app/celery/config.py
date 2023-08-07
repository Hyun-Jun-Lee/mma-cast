from app.config import (
    CELERY_CONCURRENCY,
    CELERY_NAME,
    CELERY_POOL,
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
)
from celery import Celery
from kombu import Queue


app = Celery(CELERY_NAME, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.task_default_queue = "default"
app.conf.task_queues = (
    Queue("crawling", routing_key="crawling.#"),
    Queue("transform", routing_key="transform.#"),
)
