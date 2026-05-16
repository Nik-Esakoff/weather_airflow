from datetime import datetime, timedelta
from pathlib import Path
import sys

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from weather import save_weather_to_csv

default_args = {
    "owner": "nikita",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="weather_collector",
    default_args=default_args,
    description="Collect Moscow weather every minute",
    start_date=datetime(2026, 5, 14),
    schedule="* * * * *",
    catchup=False,
    tags=["weather"],
) as dag:

    collect_weather = PythonOperator(
        task_id="collect_weather",
        python_callable=save_weather_to_csv,
    )