from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator
from dag_configs.config import default_args

with DAG(
    "financial_data_dag",
    max_active_runs=3,
    schedule_interval="0 03,15 * * *",
    default_args=default_args,
) as dag:

    t1 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="revenue_retention",
        sql="sql/financial_data/retention_wedges/revenue_retention_wedges.sql",
    )

    t2 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="logo_retention",
        sql="sql/financial_data/retention_wedges/logo_retention_wedges.sql",
    )

    t3 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="csm_customer_churn_reason",
        sql="sql/financial_data/cs/cs_customer_churn_reason.sql",
    )

    t1 >> t2
    t3