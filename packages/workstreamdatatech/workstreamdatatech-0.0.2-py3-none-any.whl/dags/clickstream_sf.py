from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from dag_configs.config import default_args
from airflow.utils.dates import days_ago

with DAG(
    "clickstream_sf_dag",
    max_active_runs=3,
    catchup=False,
    start_date=days_ago(1),
    schedule_interval="0 16,1 * * *",
    default_args=default_args,
) as dag:
    t1 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="run_base_mca_queries",
        sql="sql/channel_attribution/step001_clickstream.sql",
    )
    t1a = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="attribution_models_segment_only",
        sql="sql/channel_attribution/step002_attribution_models_segment_only.sql",
    )
    t2 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="run_base_lead_source_queries",
        sql="sql/channel_attribution/step003_lead_sources.sql",
    )

    t3 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="run_clickstream_salesforce_queries",
        sql="sql/channel_attribution/step004_linear_attribution_all_sources.sql",
    )

    t4 = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="run_campaign_queries",
        sql="sql/channel_attribution/step005_add_sf_campaigns.sql",
    )


    t1 >> t1a >> t2 >> t3 >> t4

    cut_off_date_dicts = [
        {
            "cut_off_date_col_name": "lead_created_date",
            "raw_cut_off_date_col_name": "created_date",
            "cut_off_date_table_name": "lead_create",
            "campaign_col_select_name": "loc.lead_created_date"
        },
        {
            "cut_off_date_col_name": "oppty_created_date",
            "raw_cut_off_date_col_name": "oppty_created_date",
            "cut_off_date_table_name": "oppty_create",
            "campaign_col_select_name": "lao.oppty_created_date"
        },
        {
            "cut_off_date_col_name": "closed_won_ts",
            "raw_cut_off_date_col_name": "closed_won_ts",
            "cut_off_date_table_name": "closed_won",
            "campaign_col_select_name": "lao.closed_won_ts"
        },
    ]
    end_loop = DummyOperator(task_id="end_loop")

    t6a = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="run_granular_queries",
        sql="sql/channel_attribution/step006a_granular_channel.sql",
    )

    for date_dict in cut_off_date_dicts:
        t5 = PostgresOperator(
            postgres_conn_id="postgres_db",
            task_id=f"run_attribution_queries_{date_dict['cut_off_date_col_name']}",
            sql="sql/channel_attribution/step006_linear_attribution_by_date.sql",
            params=date_dict,
            use_legacy_sql=False,
        )

        t5_parent = PostgresOperator(
            postgres_conn_id="postgres_db",
            task_id=f"run_attribution_queries_{date_dict['cut_off_date_col_name']}_parent",
            sql="sql/channel_attribution/step006_linear_attribution_parent_by_date.sql",
            params=date_dict,
            use_legacy_sql=False,
        )

        t4 >> t5 >> t5_parent >> end_loop

    end_loop >> t6a

    for date_dict in cut_off_date_dicts:
        t7 = PostgresOperator(
            postgres_conn_id="postgres_db",
            task_id=f"run_attribution_queries_{date_dict['cut_off_date_col_name']}_granular_channels",
            sql="sql/channel_attribution/step007_linear_attribution_by_date_granular.sql",
            params=date_dict,
            use_legacy_sql=False,
        )

        t8 = PostgresOperator(
            postgres_conn_id="postgres_db",
            task_id=f"run_attribution_queries_{date_dict['cut_off_date_col_name']}_team_attribution",
            sql="sql/channel_attribution/step008_linear_attribution_by_date_granular_team_attribution.sql",
            params=date_dict,
            use_legacy_sql=False,
        )

        t6a >> t7 >> t8
