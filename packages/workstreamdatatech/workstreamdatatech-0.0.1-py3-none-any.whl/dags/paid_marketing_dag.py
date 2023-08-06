from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from dag_configs.config import default_args

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2021, 6, 5),
    "schedule_interval": "0 0/12 * * *",
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

aggregation_levels = [
    {"time_delta": "1 day", "time_interval": "daily", "time_interval_noun": "day"},
    {"time_delta": "1 week", "time_interval": "weekly", "time_interval_noun": "week"},
    {
        "time_delta": "1 month",
        "time_interval": "monthly",
        "time_interval_noun": "month",
    },
]

with DAG(
    "paid_marketing_dag",
    max_active_runs=3,
    default_args=default_args,
    schedule_interval="0 0/12 * * *",
) as dag:

    start = DummyOperator(task_id="start")
    end_prep = DummyOperator(task_id="end_prep")

    raw_views = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="raw_views",
        sql="sql/paid_marketing/00_raw_views.sql",
    )

    support_tables = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="support_tables",
        sql="sql/paid_marketing/00_support_tables.sql",
    )

    clickstream_views = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="clickstream_views",
        sql="sql/paid_marketing/00_clickstream_views.sql",
    )

    start >> raw_views
    start >> support_tables >> clickstream_views
    raw_views >> clickstream_views
    clickstream_views >> end_prep

    end_loop_campaign_view = DummyOperator(task_id="end_loop_campaign_view")
    for agg in aggregation_levels:
        time_interval = agg["time_interval"]
        campaign_views = PostgresOperator(
            postgres_conn_id="postgres_db",
            task_id=f"campaign_views_{time_interval}",
            sql="sql/paid_marketing/01_paid_ads_campaign_views.sql",
            params=agg,
            use_legacy_sql=False,
        )

        end_prep >> campaign_views >> end_loop_campaign_view

    end_loop_summary_leads = DummyOperator(task_id="end_loop_summary_leads")
    for agg in aggregation_levels:
        time_interval = agg["time_interval"]
        summary_leads = PostgresOperator(
            postgres_conn_id="postgres_db",
            task_id=f"summary_leads_{time_interval}",
            sql="sql/paid_marketing/01a_paid_ads_summary_leads.sql",
            params=agg,
            use_legacy_sql=False,
        )

        end_loop_campaign_view >> summary_leads >> end_loop_summary_leads

    end_all = DummyOperator(task_id="end_all")
    for agg in aggregation_levels:
        time_interval = agg["time_interval"]
        fb_adset_views = PostgresOperator(
            postgres_conn_id="postgres_db",
            task_id=f"fb_adset_views_{time_interval}",
            sql="sql/paid_marketing/02_facebook_adset_summary.sql",
            params=agg,
            use_legacy_sql=False,
        )

        fb_ad_campaign_views = PostgresOperator(
            postgres_conn_id="postgres_db",
            task_id=f"fb_ad_campaign_views_{time_interval}",
            sql="sql/paid_marketing/03_facebook_ad_campaign_summary.sql",
            params=agg,
            use_legacy_sql=False,
        )

        end_loop_summary_leads >> fb_adset_views >> fb_ad_campaign_views >> end_all

    for agg in aggregation_levels:
        time_interval = agg["time_interval"]
        google_ad_views = PostgresOperator(
            postgres_conn_id="postgres_db",
            task_id=f"google_ad_views_{time_interval}",
            sql="sql/paid_marketing/04_google_ad_summary.sql",
            params=agg,
            use_legacy_sql=False,
        )

        google_keyword_views = PostgresOperator(
            postgres_conn_id="postgres_db",
            task_id=f"google_keyword_views_{time_interval}",
            sql="sql/paid_marketing/04_google_ad_keyword_summary.sql",
            params=agg,
            use_legacy_sql=False,
        )

        end_loop_summary_leads >> google_ad_views >> google_keyword_views >> end_all
