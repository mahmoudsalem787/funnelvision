from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

DBT = "/home/airflow/dbt_venv/bin/dbt"
DBT_DIR = "/opt/airflow/dbt_project"

default_args = {
    "owner": "mahmoud",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="funnelvision_dbt_daily",
    description="Run dbt models then dbt tests on Snowflake every day",
    default_args=default_args,
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
    tags=["funnelvision", "dbt"],
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && {DBT} run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && {DBT} test --profiles-dir .",
    )

    dbt_run >> dbt_test
