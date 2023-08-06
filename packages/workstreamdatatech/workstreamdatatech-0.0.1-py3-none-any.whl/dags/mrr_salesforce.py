from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from dag_configs.config import default_args
from airflow.models import Variable

from simple_salesforce import Salesforce

SALESFORCE_USERNAME = Variable.get("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = Variable.get("SALESFORCE_PASSWORD")
SALESFORCE_SECURITY_TOKEN = Variable.get("SALESFORCE_SECURITY_TOKEN")

sf = Salesforce(
    username=SALESFORCE_USERNAME,
    password=SALESFORCE_PASSWORD,
    security_token=SALESFORCE_SECURITY_TOKEN,
)

sql_for_plans = """with plans as (
    select
    customer_id
    , min(next_payment_date) next_payment_date
    , min(subscription_plan_interval) subscription_plan_interval
    from ws_i_existing_plans
    group by 1
)
select
      ws.salesforce_account_id
     , last_payment_date
     , last_payment_value
     , second_last_payment_date
     , second_last_payment_value
     , third_last_payment_date
     , third_last_payment_value
     , first_payment_date
     , first_payment_value
     , p.next_payment_date
     , p.subscription_plan_interval
     , total_paid_months
     , contract_end_date
     , contract_term_length
from metrics.customer_arr ca
left join metrics.ws_customers ws on ca.customer_id::text = ws.customer_id::text
left join plans p on ca.customer_id = p.customer_id
where salesforce_account_id is not null
--  and salesforce_account_id = '0016g00000sVDq7AAG'
"""


def clean_fetch_results(raw_data):
    return {
        "customer_id": raw_data[0],
        "last_payment_date": raw_data[1],
        "last_payment_value": raw_data[2],
        "second_last_payment_date": raw_data[3],
        "second_last_payment_value": raw_data[4],
        "third_last_payment_date": raw_data[5],
        "third_last_payment_value": raw_data[6],
        "first_payment_date": raw_data[7],
        "first_payment_value": raw_data[8],
        "next_payment_date": raw_data[9],
        "subscription_plan_interval": raw_data[10],
        "total_paid_months": raw_data[11],
        "contract_end_date": raw_data[12],
        "contract_term_length": raw_data[13],
    }


def format_date(date_record):
    if date_record is not None:
        return date_record.replace(microsecond=0).isoformat()
    else:
        return None


def upload_to_salesforce(raw_data, date_start):
    callback_log = []
    for i in range(len(raw_data)):
        if i % 100 == 0:
            print("Processing:", i)
        record = raw_data[i]

        customer_id = record.get("customer_id")

        data_ = {
            "Last_Payment_Date__c": format_date(record["last_payment_date"]),
            "Last_Payment_Value__c": record["last_payment_value"],
            "Second_Last_Payment_Date__c": format_date(
                record["second_last_payment_date"]
            ),
            "Second_Last_Payment_Value__c": record["second_last_payment_value"],
            "Third_Last_Payment_Date__c": format_date(
                record["third_last_payment_date"]
            ),
            "Third_Last_Payment_Value__c": record["third_last_payment_value"],
            "First_Payment_Date__c": format_date(record["first_payment_date"]),
            "First_Payment_Value__c": record["first_payment_value"],
            "Next_Payment_Date__c": format_date(record["next_payment_date"]),
            "subscription_length__c": record["subscription_plan_interval"],
            "payment_data_last_updated__c": datetime.now().isoformat(),
            "Total_Months_Paid__c": record["total_paid_months"],
            "Contract_End_Date__c": format_date(record["contract_end_date"]),
            "Contract_Term_Length__c": record["contract_term_length"],
        }

        # print(data_)
        try:
            callback_message = sf.Account.update(customer_id, data_)
            callback_log.append(
                {
                    "record_id": customer_id,
                    "message": str(callback_message),
                    "record_type": "account",
                    "run_ts": date_start,
                    "current_ts": datetime.now().isoformat(),
                }
            )
        except Exception as e:
            callback_log.append(
                {
                    "record_id": customer_id,
                    "message": str(e),
                    "record_type": "Account",
                    "run_ts": date_start,
                    "current_ts": datetime.now().isoformat(),
                }
            )
    return callback_log


def run_sf_push(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id="postgres_db")
    cur = pg_hook.get_cursor()
    execution = cur.execute(kwargs["sql_for_plans"])
    postgres_results = cur.fetchall()
    print("number of results: ", len(postgres_results))
    results_dict = list(map(clean_fetch_results, postgres_results))

    callback_log = upload_to_salesforce(results_dict, kwargs["date_start"])
    print("finished pushing to salesforce")

    insert_statement = """INSERT INTO callbacks.lead_source_salesforce VALUES \
    (%(record_id)s, %(record_type)s, %(message)s, %(run_ts)s,%(current_ts)s  );
    commit;
    """
    cur.executemany(insert_statement, callback_log)
    print("finish pushing errors to db")
    cur.close()
    return


dag = DAG("mrr_salesforce", default_args=default_args)

push_to_sf = PythonOperator(
    task_id="push_to_sf_mrr",
    python_callable=run_sf_push,
    provide_context=True,
    op_kwargs={"sql_for_plans": sql_for_plans, "date_start": "{{ ds }}"},
    dag=dag,
)

push_to_sf
