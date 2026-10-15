FROM apache/airflow:2.10.5-python3.11

USER airflow

RUN python -m venv /home/airflow/dbt_venv \
    && /home/airflow/dbt_venv/bin/pip install --no-cache-dir --upgrade pip \
    && /home/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-snowflake==1.9.0
    