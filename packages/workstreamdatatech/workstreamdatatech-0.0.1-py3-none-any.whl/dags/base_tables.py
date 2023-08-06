from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator
from dag_configs.config import default_args
from airflow.utils.dates import days_ago

with DAG(
    "base_table_dag",
    max_active_runs=3,
    catchup=False,
    start_date=days_ago(1),
    schedule_interval=timedelta(hours=3),
    default_args=default_args,
) as dag:

    t1 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="customers",
        sql="sql/customers/all_customers.sql",
    )

    t2 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="transactions",
        sql="sql/transactions/all_transactions_revenue_components.sql",
    )

    t3 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="mtd_customers",
        sql="sql/mtd_customers/mtd_customers.sql",
    )

    t4 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="revenue_retention_account_manager",
        sql="sql/transactions/revenue_retention_account_manager.sql",
    )

    t1 >> t2 >> t3 >> t4
