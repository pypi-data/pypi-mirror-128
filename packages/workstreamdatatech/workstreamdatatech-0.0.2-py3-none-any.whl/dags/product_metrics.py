from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator
from dag_configs.config import default_args

with DAG(
    "product_metrics_dag",
    max_active_runs=3,
    schedule_interval=timedelta(hours=3),
    default_args=default_args,
) as dag:

    t1 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="run_product_metric_queries",
        sql="sql/product_metrics/users_and_review.sql",
    )

    t2 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="run_quick_review_indiv",
        sql="sql/product_metrics/quick_review.sql",
    )

    t3 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="run_hired_indiv",
        sql="sql/product_metrics/hired.sql",
    )

    t4 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="mobile_indiv",
        sql="sql/product_metrics/mobile_views.sql",
    )
    t5 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="all_page_views",
        sql="sql/product_metrics/all_page_views.sql",
    )

    t6 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="sign_in_review",
        sql="sql/product_metrics/sign_in_review.sql",
    )

    t7 = PostgresOperator(
            postgres_conn_id="postgres_db",
            task_id="locations_users",
            sql="sql/product_metrics/locations_users.sql",
    )

    t8 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="cos_metrics_1",
        sql="sql/product_metrics/cos_metrics_1.sql",
    )

    t9 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="cos_metrics_2",
        sql="sql/product_metrics/cos_metrics_2.sql",
    )

    t10 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="cos_metrics_3",
        sql="sql/product_metrics/cos_metrics_3.sql",
    )

    t11 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="cos_metrics_4",
        sql="sql/product_metrics/cos_metrics_4.sql",
    )

    t12 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="applicant_metrics",
        sql="sql/product_metrics/applicant_metrics.sql",
    )

    t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7 >> t8 >> t9 >> t10 >> t11 >> t12
