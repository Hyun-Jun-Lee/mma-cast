from datetime import datetime, timedelta
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from async_data_crawling import run_craw_game

default_args = {
    "owner": "mma_cast",
    "depends_on_past": False,
    "start_date": datetime(2023, 7, 14),
    "email": ["bhk0827@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    # 'adhoc':False,
}

dag = DAG(
    "crawling",
    default_args=default_args,
    description="crawling UFC Stat",
    schedule="0 9 * * *",
)

crawl_task = PythonOperator(
    task_id="crawl_ufc_data_task",
    python_callable=run_craw_game,
    dag=dag,
)

crawl_task
