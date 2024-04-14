from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from tasks.utils import check_connection
from tasks.ufc_data_crawling import (
    execute_fighter_info_fetching,
    execute_match_info_fetching,
)


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
    "ufc_crawling",
    default_args=default_args,
    description="crawling UFC Stat",
    schedule="0 9 * * *",
)

check_connection_task = PythonOperator(
    task_id="check_mongodb_connection",
    python_callable=check_connection,
    dag=dag,
)


crawl_game_task = PythonOperator(
    task_id="crawl_games",
    python_callable=execute_match_info_fetching,
    dag=dag,
)

crawl_fighter_task = PythonOperator(
    task_id="crawl_fighter",
    python_callable=execute_fighter_info_fetching,
    dag=dag,
)


check_connection_task >> crawl_game_task >> crawl_fighter_task
