from datetime import datetime
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable
from simple_salesforce import Salesforce
from dag_configs.config import default_args

SALESFORCE_USERNAME = Variable.get("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = Variable.get("SALESFORCE_PASSWORD")
SALESFORCE_SECURITY_TOKEN = Variable.get("SALESFORCE_SECURITY_TOKEN")

sf = Salesforce(
    username=SALESFORCE_USERNAME,
    password=SALESFORCE_PASSWORD,
    security_token=SALESFORCE_SECURITY_TOKEN,
)


col_mapping = {
    "customer_id": "Workstream_Customer_ID__c",
    "company_product_tiers" : "Product_Tier__c",
    "salesforce_id": "salesforce_id",
    "onboarding_yn": "Access_to_Onboarding__c",
    "last_seen": "Last_Seen__c",
    "last_login_at": "Last_Login__c",
    "total_hires": "Number_of_Applicants_Hired__c",
    "hires_7_days": "Number_of_Hires_Last_7_Days__c",
    "hires_14_days": "Number_of_Hires_Last_14_Days__c",
    "hires_30_days": "Number_of_Hires_Last_30_Days__c",
    "total_locations": "Total_of_Locations__c",
    "locations_7_days": "Total_of_Locations_Added_Last_7_Days__c",
    "locations_14_days": "Total_of_Locations_Added_Last_14_Days__c",
    "locations_30_days": "Total_of_Locations_Added_Last_30_Days__c",
    "interviews_confirmed_7_days": "Interviews_Upcoming_Week__c",
    "interviews_confirmed_14_days": "of_Interviews_Next_2_Weeks__c",
    "no_show_app_stages_7_days": "of_No_Show_Applicants_Last_7_Days__c",
    "no_show_app_stages_14_days": "of_No_Show_Applicants_Last_14_Days__c",
    "no_show_app_stages_30_days": "of_No_Show_Applicants_Last_30_Days__c",
    "no_show_app_stages_total": "Number_of_Applicants_Tagged_as_No_Show__c",
    "complete_app_stages_7_days": "of_Applicants_Interview_Complete_L7D__c",
    "complete_app_stages_14_days": "of_Applicants_Interview_Complete_L14D__c",
    "complete_app_stages_30_days": "of_Applicants_Interview_Complete_L30D__c",
    "complete_app_stages_total": "of_Applicants_w_Interview_Complete__c",
    "total_applicants": "Total_of_Applicants__c",
    "applicants_7_days": "Number_of_Applicants_Past_7_Days__c",
    "applicants_14_days": "of_Applicants_Last_14_Days__c",
    "applicants_30_days": "of_Applicants_Last_30_Days__c",
    "total_indeed_applicants": "of_Applicants_Indeed__c",
    "indeed_applicants_7_days": "of_Applicants_Last_7_Days_Indeed__c",
    "indeed_applicants_14_days": "of_Applicants_Last_14_Days_Indeed__c",
    "indeed_applicants_30_days": "of_Applicants_Last_30_Days_Indeed__c",
    "first_referer_source": "X1_Applicant_Source__c",
    "first_referer_source_applicants": "Applicants_from_1_Source__c",
    "second_referer_source": "X2_Applicant_Source__c",
    "second_referer_source_applicants": "Applicants_from_2_Source__c",
    "third_referer_source": "X3_Applicant_Source__c",
    "third_referer_source_applicants": "Applicants_from_3_Source__c",
    "num_applicant_moved_7_days": "of_Applicants_Moved_Manually_L7D__c",
    "num_applicant_moved_14_days": "of_Applicants_Moved_Manually_L14D__c",
    "num_applicant_moved_30_days": "of_Applicants_Moved_Manually_L30D__c",
    "num_auto_reject": "Number_of_Applicants_Auto_Rejected__c",
    "num_auto_reject_7_days": "Number_of_Applicants_Auto_Rejected_L7D__c",
    "num_auto_reject_14_days": "Number_of_Applicants_Auto_Rejected_L14D__c",
    "num_auto_reject_30_days": "Number_of_Applicants_Auto_Rejected_L30D__c",
    "rejected_applicants_total": "Number_of_Applicants_Rejected__c",
    "rejected_applicants_7_days": "Number_of_Applicants_Rejected_L7D__c",
    "rejected_applicants_14_days": "Number_of_Applicants_Rejected_L14D__c",
    "rejected_applicants_30_days": "Number_of_Applicants_Rejected_L30D__c",
    "total_published_positions": "Number_of_Published_Positions__c",
    "total_positions": "Number_of_Total_Positions__c",
    "positions_7_days": "Number_of_Positions_Added_Last_7_Days__c",
    "positions_14_days": "Number_of_Positions_Added_Last_14_Days__c",
    "positions_30_days": "Number_of_Positions_Added_Last_30_Days__c",
    "manual_sms_7_days": "of_Manual_Texts_Sent_Last_7_Days__c",
    "manual_sms_14_days": "of_Manual_Texts_Sent_Last_14_Days__c",
    "manual_sms_30_days": "of_Manual_Texts_Sent_Last_30_Days__c",
    "avg_num_questions_pos": "Mean_of_Screener_Questions_by_Position__c",
    "avg_num_questions_form": "Mean_of_Questions_in_a_Form_Stage__c",
    "avg_num_stages": "Mean_of_Stages_by_Position__c",
    "avg_manual_stages": "Mean_of_Manual_Stages_in_an_Account__c",
    "avg_num_days_in_progress": "Mean_of_Applicants_Days_In_Progress__c",
    "intercom_msgs_7_days": "of_Intercom_Messages_Received_L7D__c",
    "intercom_msgs_14_days": "of_Intercom_Messages_Received_L14D__c",
    "intercom_msgs_30_days": "of_Intercom_Messages_Received_L30D__c",
    "open_intercom_msgs": "Number_of_Open_Intercom_Messages__c",
    "total_user_count": "of_Users__c",
    "admin_role_count": "Number_of_Admins__c",
    "super_admin_role_count": "Number_of_Super_Admins__c",
    "user_role_count": "Number_of_Team_Members__c",
    "nps_7_days": "NPS_Score_Last_7_Days__c",
    "nps_14_days": "NPS_Score_Last_14_Days__c",
    "nps_30_days": "NPS_Score_Last_30_Days__c",
    "annual_contract_end_date": "Contract_End_Date__c",
    "moonclerk_plan_count": "Active_Moonclerk_Plan_Count__c",
    "internal_billing_plan_count": "Active_Internal_Billing_Plan_Count__c",
    "last_payment_value": "Last_Payment_Value__c",
    "last_payment_date": "Last_Payment_Date__c",
    "first_payment_value": "First_Payment_Value__c",
    "first_payment_date": "First_Payment_Date__c",
    "total_paid_months": "Total_Months_Paid__c",
    "admin_url": "Workstream_Customer_Page__c",
    "run_time": "Product_data_last_updated__c",
    "pct_position_timeslot_created": "Jobs_w_Interview_Stage_No_Timeslots__c",
}


main_sql = """
select 
    customer_id
     , company_product_tiers
     , salesforce_account_id
     , onboarding_yn
     , last_seen
     , last_login_at
     , total_hires
     , hires_7_days
     , hires_14_days
     , hires_30_days
     , total_locations
     , locations_7_days
     , locations_14_days
     , locations_30_days
     , interviews_confirmed_7_days
     , interviews_confirmed_14_days
     , no_show_app_stages_7_days
     , no_show_app_stages_14_days
     , no_show_app_stages_30_days
     , no_show_app_stages_total
     , complete_app_stages_7_days
     , complete_app_stages_14_days
     , complete_app_stages_30_days
     , complete_app_stages_total
     , total_applicants
     , applicants_7_days
     , applicants_14_days
     , applicants_30_days
     , total_indeed_applicants
     , indeed_applicants_7_days
     , indeed_applicants_14_days
     , indeed_applicants_30_days
     , first_referer_source
     , first_referer_source_applicants
     , second_referer_source
     , second_referer_source_applicants
     , third_referer_source
     , third_referer_source_applicants
     , num_applicant_moved_7_days
     , num_applicant_moved_14_days
     , num_applicant_moved_30_days
     , num_auto_reject
     , num_auto_reject_7_days
     , num_auto_reject_14_days
     , num_auto_reject_30_days
     , rejected_applicants_total
     , rejected_applicants_7_days
     , rejected_applicants_14_days
     , rejected_applicants_30_days
     , total_published_positions
     , total_positions
     , positions_7_days
     , positions_14_days
     , positions_30_days
     , manual_sms_7_days
     , manual_sms_14_days
     , manual_sms_30_days
     , avg_num_questions_pos
     , avg_num_questions_form
     , avg_num_stages
     , avg_manual_stages
     , avg_num_days_in_progress
     , intercom_msgs_7_days
     , intercom_msgs_14_days
     , intercom_msgs_30_days
     , open_intercom_msgs
     , total_user_count
     , admin_role_count
     , super_admin_role_count
     , user_role_count
     , nps_7_days
     , nps_14_days
     , nps_30_days
     , annual_contract_end_date
     , moonclerk_plan_count
     , internal_billing_plan_count
     , last_payment_value
     , last_payment_date
     , first_payment_value
     , first_payment_date
     , total_paid_months
     , admin_url
     , run_time
     , pct_position_timeslot_created
 from metrics.sf_customer_metrics

"""
col_order = [
    "customer_id",
    "company_product_tiers",
    "salesforce_id",
    "onboarding_yn",
    "last_seen",
    "last_login_at",
    "total_hires",
    "hires_7_days",
    "hires_14_days",
    "hires_30_days",
    "total_locations",
    "locations_7_days",
    "locations_14_days",
    "locations_30_days",
    "interviews_confirmed_7_days",
    "interviews_confirmed_14_days",
    "no_show_app_stages_7_days",
    "no_show_app_stages_14_days",
    "no_show_app_stages_30_days",
    "no_show_app_stages_total",
    "complete_app_stages_7_days",
    "complete_app_stages_14_days",
    "complete_app_stages_30_days",
    "complete_app_stages_total",
    "total_applicants",
    "applicants_7_days",
    "applicants_14_days",
    "applicants_30_days",
    "total_indeed_applicants",
    "indeed_applicants_7_days",
    "indeed_applicants_14_days",
    "indeed_applicants_30_days",
    "first_referer_source",
    "first_referer_source_applicants",
    "second_referer_source",
    "second_referer_source_applicants",
    "third_referer_source",
    "third_referer_source_applicants",
    "num_applicant_moved_7_days",
    "num_applicant_moved_14_days",
    "num_applicant_moved_30_days",
    "num_auto_reject",
    "num_auto_reject_7_days",
    "num_auto_reject_14_days",
    "num_auto_reject_30_days",
    "rejected_applicants_total",
    "rejected_applicants_7_days",
    "rejected_applicants_14_days",
    "rejected_applicants_30_days",
    "total_published_positions",
    "total_positions",
    "positions_7_days",
    "positions_14_days",
    "positions_30_days",
    "manual_sms_7_days",
    "manual_sms_14_days",
    "manual_sms_30_days",
    "avg_num_questions_pos",
    "avg_num_questions_form",
    "avg_num_stages",
    "avg_manual_stages",
    "avg_num_days_in_progress",
    "intercom_msgs_7_days",
    "intercom_msgs_14_days",
    "intercom_msgs_30_days",
    "open_intercom_msgs",
    "total_user_count",
    "admin_role_count",
    "super_admin_role_count",
    "user_role_count",
    "nps_7_days",
    "nps_14_days",
    "nps_30_days",
    "annual_contract_end_date",
    "moonclerk_plan_count",
    "internal_billing_plan_count",
    "last_payment_value",
    "last_payment_date",
    "first_payment_value",
    "first_payment_date",
    "total_paid_months",
    "admin_url",
    "run_time",
    "pct_position_timeslot_created",
]


def clean_fetch_results(raw_data):
    return {col_mapping[k]: v for k, v in dict(zip(col_order, raw_data)).items()}


def format_date(date_record):
    if date_record is not None:
        return date_record.replace(microsecond=0).isoformat()
    else:
        return None


def format_data(input_dict):
    date_cols = [
        "Contract_End_Date__c",
        "Last_Seen__c",
        "Last_Login__c",
        "Last_Payment_Date__c",
        "First_Payment_Date__c",
        "Next_Payment_Date__c",
        "Product_data_last_updated__c",
    ]
    decimal_cols = [
        "Mean_of_Screener_Questions_by_Position__c",
        "Mean_of_Questions_in_a_Form_Stage__c",
        "Mean_of_Stages_by_Position__c",
        "NPS_Score_Last_14_Days__c",
        "NPS_Score_Last_30_Days__c",
        "NPS_Score_Last_7_Days__c",
        "Mean_of_Manual_Stages_in_an_Account__c",
        "Mean_of_Applicants_Days_In_Progress__c",
    ]
    source_cols = [
        "X1_Applicant_Source__c",
        "X2_Applicant_Source__c",
        "X3_Applicant_Source__c",
    ]
    output_dict = {}
    for k, v in input_dict.items():
        if v != None:
            if k in date_cols:
                v = format_date(v)
            if k in decimal_cols:
                v = float(v)
            if k in source_cols:
                v = v[:255]
            if k == "Access_to_Onboarding__c":
                if v == 1:
                    v = "Yes"
                if v == 0:
                    v = "No"
            output_dict[k] = v

    return output_dict


def upload_to_salesforce(raw_data):
    callback_log = []
    for i in range(len(raw_data)):
        if i % 100 == 0:
            print("Processing:", i)
        record = raw_data[i]

        customer_id = record.get("salesforce_id")
        data_ = {
            k: record[k] for k in col_mapping.values() if k not in ("salesforce_id")
        }
        input_data = format_data(data_)
        print(input_data)
        try:
            callback_message = sf.Account.update(customer_id, input_data)
            callback_log.append(
                {
                    "record_id": customer_id,
                    "message": str(callback_message),
                    "record_type": "account",
                    "run_ts": dag_params["start_date"].strftime("%Y-%m-%d"),
                    "current_ts": datetime.now().isoformat(),
                }
            )
        except Exception as e:
            print(input_data)
            print("ERROR: ", customer_id, str(e))
            callback_log.append(
                {
                    "record_id": customer_id,
                    "message": str(e),
                    "record_type": "Account",
                    "run_ts": dag_params["start_date"].strftime("%Y-%m-%d"),
                    "current_ts": datetime.now().isoformat(),
                }
            )
    return callback_log


def run_sf_push(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id="postgres_db")
    cur = pg_hook.get_cursor()
    execution = cur.execute(kwargs["main_sql"])
    postgres_results = cur.fetchall()
    print("number of results: ", len(postgres_results))
    results_dict = list(map(clean_fetch_results, postgres_results))

    callback_log = upload_to_salesforce(results_dict)
    print("finished pushing to salesforce")

    insert_statement = """INSERT INTO callbacks.lead_source_salesforce VALUES \
    (%(record_id)s, %(record_type)s, %(message)s, %(run_ts)s,%(current_ts)s  );
    commit;
    """
    cur.executemany(insert_statement, callback_log)
    print("finish pushing errors to db")
    cur.close()
    return


dag_params = {"start_date": datetime(2021, 2, 17)}


dag = DAG("customer_usage_sf", schedule_interval="@hourly", default_args=default_args)

run_sql = PostgresOperator(
    postgres_conn_id="postgres_db",
    task_id="run_product_sql",
    sql="sql/product_metrics/sf_product_metrics_1.sql",
    dag=dag,
)

run_sql_1b = PostgresOperator(
    postgres_conn_id="postgres_db",
    task_id="run_product_sql_1b",
    sql="sql/product_metrics/sf_product_metrics_1_b.sql",
    dag=dag,
)

run_sql_2 = PostgresOperator(
    postgres_conn_id="postgres_db",
    task_id="run_product_sql_2",
    sql="sql/product_metrics/sf_product_metrics_2.sql",
    dag=dag,
)

push_to_sf = PythonOperator(
    task_id="push_to_sf_usage",
    python_callable=run_sf_push,
    provide_context=True,
    op_kwargs={"main_sql": main_sql},
    dag=dag,
)

run_sql >> run_sql_1b >> run_sql_2 >> push_to_sf
