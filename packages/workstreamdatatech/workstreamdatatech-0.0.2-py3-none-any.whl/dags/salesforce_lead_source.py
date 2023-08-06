from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable
from dag_configs.config import default_args
from simple_salesforce import Salesforce

SALESFORCE_USERNAME = Variable.get("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = Variable.get("SALESFORCE_PASSWORD")
SALESFORCE_SECURITY_TOKEN = Variable.get("SALESFORCE_SECURITY_TOKEN")

sf = Salesforce(
    username=SALESFORCE_USERNAME,
    password=SALESFORCE_PASSWORD,
    security_token=SALESFORCE_SECURITY_TOKEN,
)


dag_params = {
    "dag_id": "lead_salesforce",
    "start_date": datetime(2020, 12, 3),
    "schedule_interval": "0 */12 * * *",
}

day_margin = "3 days"

sql_for_lead = """
with last_change_opp as (
    select distinct opportunity_id
    from salesforce.opportunity_field_history
    where field in ('Where_did_they_hear_about_us__c', 'LeadSource', 'Lead_Source_Detail__c')
    and created_date between '{{ ds }}'::date - interval '{day_margin}' and '{{ ds }}'::date + interval '{day_margin}'
)
   , last_change_lead as (
    select distinct lead_id
    from salesforce.lead_history
    where field in ('Where_did_they_hear_about_us__c', 'LeadSource', 'Lead_Source_Detail__c')
      and created_date between '{{ ds }}'::date - interval '{day_margin}' and '{{ ds }}'::date + interval '{day_margin}'
)
   , oppty_create as (
    select lead_id
         , opportunity_id
         , array_agg(linear_channel_type) linear_channels
    from source_attribution.lead_opp_linear_attribution_oppty_create
    group by 1, 2
)
   , oppty_close as (
    select lead_id
         , opportunity_id
         , array_agg(linear_channel_type) linear_channels
    from source_attribution.lead_opp_linear_attribution_closed_won
    group by 1, 2
)
select la.lead_id
     , la.opportunity_id
     , segment_last_touch_source_type_summary
     , segment_last_touch_source_type
     , segment_last_touch_source_type_timestamp
     , segment_first_touch_source_type
     , segment_first_touch_source_type_summary
     , segment_first_touch_source_type_timestamp
     , hubspot_lead_source_1
     , salesforce_lead_source_1
     , final_source_type_first_touch
     , final_channel_first_touch
     , final_source_type_last_touch
     , final_channel_last_touch
     , case when la.closed_won_ts is not null then array_to_string(oc.linear_channels,',') else array_to_string(o.linear_channels,',') end linear_channels
from cac.lead_all_opps la
         left join last_change_opp lo on la.opportunity_id = lo.opportunity_id
         left join last_change_lead ll on la.lead_id = ll.lead_id
         left join oppty_create o on case
                                         when o.opportunity_id is not null then la.opportunity_id = o.opportunity_id
                                         else la.lead_id = o.lead_id end
         left join oppty_close oc on closed_won_ts is not null and la.opportunity_id = oc.opportunity_id
where 1 = 1 and 
         (lo.opportunity_id is not null or ll.lead_id is not null)
         or (la.created_date between '{{ ds }}'::date - interval '{day_margin}' and '{{ ds }}'::date + interval '{day_margin}'
         or la.oppty_created_date between '{{ ds }}'::date - interval '{day_margin}' and '{{ ds }}'::date + interval '{day_margin}' )  
    """

print("SQL", sql_for_lead)


def clean_fetch_results(raw_data):
    return {
        "lead_id": raw_data[0],
        "opportunity_id": raw_data[1],
        "segment_last_touch_source_type_summary": raw_data[2],
        "segment_last_touch_source_type": raw_data[3],
        "segment_last_touch_source_type_timestamp": raw_data[4],
        "segment_first_touch_source_type": raw_data[5],
        "segment_first_touch_source_type_summary": raw_data[6],
        "segment_first_touch_source_type_timestamp": raw_data[7],
        "hubspot_lead_source_1": raw_data[8],
        "salesforce_lead_source_1": raw_data[9],
        "final_source_type_first_touch": raw_data[10],
        "final_channel_first_touch": raw_data[11],
        "final_source_type_last_touch": raw_data[12],
        "final_channel_last_touch": raw_data[13],
        "linear_channels": raw_data[14],
    }


def format_date(date_record):
    if date_record is not None:
        return date_record.replace(microsecond=0).isoformat()
    else:
        return None


def drop_null_value_keys(input_dict):
    result_dict = {}
    for key in input_dict.keys():
        item = input_dict[key]
        if item is not None:
            result_dict[key] = item
    return result_dict


def upload_to_salesforce(raw_data, execution_time):
    callback_log = []
    for i in range(len(raw_data)):
        record = raw_data[i]

        # if opportunity id exists, update the opportunity, if not, update the lead

        get_oppty_id = record.get("opportunity_id")
        if get_oppty_id:
            record_id = get_oppty_id
            record_type = "oppty"
            # on the oppty level, segment source field has a diff name
            segment_raw_source_field_name = "Segment_Last_Touch_Raw_Source__c"
        else:
            record_id = record.get("lead_id")
            record_type = "lead"
            segment_raw_source_field_name = "Segment_Last_Touch_Raw_Source2__c"

        data_ = {
            "Segment_Last_Touch_Summarized_Source__c": record[
                "segment_last_touch_source_type_summary"
            ],
            segment_raw_source_field_name: record["segment_last_touch_source_type"],
            "Segment_Last_Touch_Source_Timestamp__c": format_date(
                record["segment_last_touch_source_type_timestamp"]
            ),
            "Segment_First_Touch_Raw_Source__c": record[
                "segment_first_touch_source_type"
            ],
            "Segment_First_Touch_Summarized_Source__c": record[
                "segment_first_touch_source_type_summary"
            ],
            "Segment_First_Touch_Source_Timestamp__c": format_date(
                record["segment_first_touch_source_type_timestamp"]
            ),
            "Hubspot_Summarized_Source__c": record["hubspot_lead_source_1"],
            "Salesforce_Summarized_Source__c": record["salesforce_lead_source_1"],
            "Final_First_Touch_Source__c": record["final_source_type_first_touch"],
            "Final_First_Touch_Channel__c": record["final_channel_first_touch"],
            "Final_Last_Touch_Source__c": record["final_source_type_last_touch"],
            "Final_Last_Touch_Channel__c": record["final_channel_last_touch"],
            "Linear_Attribution_Channels__c": record["linear_channels"],
        }
        data_filter = drop_null_value_keys(data_)
        #         print('this is the data', data_filter)
        try:
            if record_type == "oppty":
                callback_message = sf.Opportunity.update(record_id, data_filter)
            elif record_type == "lead":
                callback_message = sf.Lead.update(record_id, data_filter)
            callback_log.append(
                {
                    "record_id": record_id,
                    "message": str(callback_message),
                    "record_type": record_type,
                    "run_ts": execution_time,
                    "current_ts": datetime.now().isoformat(),
                }
            )
        except Exception as e:
            callback_log.append(
                {
                    "record_id": record_id,
                    "message": str(e),
                    "record_type": record_type,
                    "run_ts": execution_time,
                    "current_ts": datetime.now().isoformat(),
                }
            )
    return callback_log


def run_sf_push(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id="postgres_db")
    cur = pg_hook.get_cursor()
    execution = cur.execute(kwargs["sql_for_lead"].format(day_margin=day_margin))
    postgres_results = cur.fetchall()
    print("number of results: ", len(postgres_results))
    results_dict = list(map(clean_fetch_results, postgres_results))

    callback_log = upload_to_salesforce(results_dict, kwargs["execution_time"])
    print("finished pushing to salesforce")

    insert_statement = """INSERT INTO callbacks.lead_source_salesforce VALUES \
    (%(record_id)s, %(record_type)s, %(message)s, %(run_ts)s,%(current_ts)s  );
    commit;
    """
    cur.executemany(insert_statement, callback_log)
    print("finish pushing errors to db")
    cur.close()
    return


sql_for_lead_individual_check = """with last_change_opp as (
    select distinct opportunity_id
    from salesforce.opportunity_field_history
    where field in ('Where_did_they_hear_about_us__c', 'LeadSource', 'Lead_Source_Detail__c')
--     and created_date between '{{ ds }}'::date - interval '{day_margin}' and '{{ ds }}'::date + interval '{day_margin}'
)
   , last_change_lead as (
    select distinct lead_id
    from salesforce.lead_history
    where field in ('Where_did_they_hear_about_us__c', 'LeadSource', 'Lead_Source_Detail__c')
--       and created_date between '{{ ds }}'::date - interval '{day_margin}' and '{{ ds }}'::date + interval '{day_margin}'
)
   , oppty_create as (
    select lead_id
         , opportunity_id
         , array_agg(linear_channel_type) linear_channels
    from source_attribution.lead_opp_linear_attribution_oppty_create
    group by 1, 2
)
   , oppty_close as (
    select lead_id
         , opportunity_id
         , array_agg(linear_channel_type) linear_channels
    from source_attribution.lead_opp_linear_attribution_closed_won
    group by 1, 2
)
select la.lead_id
     , la.opportunity_id
     , segment_last_touch_source_type_summary
     , segment_last_touch_source_type
     , segment_last_touch_source_type_timestamp
     , segment_first_touch_source_type
     , segment_first_touch_source_type_summary
     , segment_first_touch_source_type_timestamp
     , hubspot_lead_source_1
     , salesforce_lead_source_1
     , final_source_type_first_touch
     , final_channel_first_touch
     , final_source_type_last_touch
     , final_channel_last_touch
     , case when la.closed_won_ts is not null then array_to_string(oc.linear_channels,',') else array_to_string(o.linear_channels,',') end linear_channels
from cac.lead_all_opps la
         left join last_change_opp lo on la.opportunity_id = lo.opportunity_id
         left join last_change_lead ll on la.lead_id = ll.lead_id
         left join oppty_create o on case
                                         when o.opportunity_id is not null then la.opportunity_id = o.opportunity_id
                                         else la.lead_id = o.lead_id end
         left join oppty_close oc on closed_won_ts is not null and la.opportunity_id = oc.opportunity_id
where 1 = 1 and
      la.lead_id='00Q6g00000EyQkIEAV'
"""


dag = DAG(
    "lead_salesforce",
    default_args=default_args,
    schedule_interval="0 */12 * * *",
)

push_to_sf = PythonOperator(
    task_id="push_to_sf",
    python_callable=run_sf_push,
    provide_context=True,
    op_kwargs={"sql_for_lead": sql_for_lead, "execution_time": "{{ ds }}"},
    dag=dag,
)

push_to_sf
