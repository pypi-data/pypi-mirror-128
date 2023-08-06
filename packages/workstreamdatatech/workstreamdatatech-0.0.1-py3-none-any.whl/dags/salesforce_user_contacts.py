from datetime import datetime
from collections import defaultdict
from typing import Type, List, Dict, Optional
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import (
    SalesforceResourceNotFound,
    SalesforceMoreThanOneRecord,
)
from dag_configs.config import default_args
import logging
from sql.user_contacts.sf_user_contacts_query import query_string
from plugins.functions.sql_format import transform_to_dict

SALESFORCE_USERNAME = Variable.get("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = Variable.get("SALESFORCE_PASSWORD")
SALESFORCE_SECURITY_TOKEN = Variable.get("SALESFORCE_SECURITY_TOKEN")


######################################################
# Data cleaning
######################################################


def format_date(date_record: str) -> Optional[str]:
    if date_record is not None:
        return date_record.replace(microsecond=0).isoformat()
    else:
        return None

def transform_to_email_dict(input_list: List) -> Dict[str, str]:
    output_dict = defaultdict(str)
    for elem in input_list:
        output_dict[elem["Email"]] = elem["Id"]
    return output_dict

def format_data(input_dict) -> Dict:
    date_cols = ["User_Created_Date__c", "Last_Seen__c", "Automated_Conversion_Date__c"]
    bool_cols = [
        "User_Onboard_Employee__c",
        "User_All_Admin_Rights__c",
    ]
    output_dict = {}
    for k, v in input_dict.items():
        if k.startswith('info') or v is None:
            continue
        if k in bool_cols:
            v = "Yes" if v == 1 else "No"
        elif k in date_cols:
            v = format_date(v)

        output_dict[k] = v

    return output_dict


def lead_exists(email: str, salesforce_connection: Type[Salesforce],
                lead_email_dict: Dict,
                contact_email_list: Dict
                ) -> Optional[str]:
    """
    If the email is only associated with lead and not a contact object, will return the lead id, otherwise none.
    """
    record_contact_id, record_lead_id = None, None

    record_lead_id = lead_email_dict.get(email)
    print(f"lead_id {record_lead_id}")

    record_contact_id = contact_email_list.get(email)
    print(f"contact_id {record_contact_id}")

    # returns lead id if no contact object is returned, only lead object for given email
    if record_contact_id is None and record_lead_id is not None:
        return record_lead_id
    else:
        return None


def convert_lead(lead_id: str, account_id, salesforce_connection: Type[Salesforce]):
    res = salesforce_connection.apexecute(f"LeadConvertWithAccount/LeadId={lead_id}&AccountId={account_id}", method="GET")
    if res == "fail":
        update_res = salesforce_connection.Lead.update(lead_id, {"LeadSource": "Other"})
        print(update_res)
        res = salesforce_connection.apexecute(f"LeadConvertWithAccount/LeadId={lead_id}&AccountId={account_id}", method="GET")
    return res


######################################################
# Process sql results and push to salesforce
######################################################


def upload_contact_to_salesforce(raw_data: List[Dict]) -> List:

    sf = Salesforce(
        username=SALESFORCE_USERNAME,
        password=SALESFORCE_PASSWORD,
        security_token=SALESFORCE_SECURITY_TOKEN,
    )

    lead_query = 'SELECT ID, Email FROM Lead where IsDeleted=False'
    contact_query = 'SELECT ID, Email FROM Contact where IsDeleted=False'

    all_leads = sf.bulk.Lead.query(lead_query)
    all_contacts = sf.bulk.Contact.query(contact_query)

    all_leads_dict = transform_to_email_dict(all_leads)
    all_contacts_dict = transform_to_email_dict(all_contacts)
    formatted_data = [format_data(elem) for elem in raw_data]

    # split formatted data list into leads that need to be converted vs only exist as contacts
    lead_convert_list, lead_non_convert_list = [], []
    for record in formatted_data:
        if all_leads_dict.get(record["Email"]) is not None and all_contacts_dict.get(record["Email"]) is None:
            lead_convert_list.append(record)
        else:
            lead_non_convert_list.append(record)

    # convert all emails one by one (no bulk api call possible for custom apex classes)
    contacts_from_lead_convert_list = []
    for i, record in enumerate(lead_convert_list):
        if i % 100 == 0:
            print("Processing:", i)
        record_email = record["Email"]
        record_accountId = record["AccountId"]
        record_lead_id_to_convert = all_leads_dict.get(record_email)
        # api call to convert lead to a contact
        convert_callback = convert_lead(record_lead_id_to_convert, record_accountId, sf)
        logging.info(
            f"Lead with email {record_email} converted status: {convert_callback}"
        )
        record["Automated_Conversion_Date__c"] = datetime.utcnow()
        contacts_from_lead_convert_list.append(record)

    complete_payload = lead_non_convert_list + contacts_from_lead_convert_list
    callback = sf.bulk.Contact.upsert(complete_payload, 'Email', batch_size=1000, use_serial=True)
    logging.info("Callback Results: ")
    logging.info(callback)

def run_sf_push(**kwargs) -> None:
    pg_hook = PostgresHook(postgres_conn_id="postgres_db")
    cur = pg_hook.get_cursor()
    execution = cur.execute(
        query_string.format(execution_date=kwargs["execution_date"])
    )
    col_names = [desc[0] for desc in cur.description]
    query_results = cur.fetchall()
    logging.info(f"number of contacts: {len(query_results)}")
    results_dict = transform_to_dict(query_results, col_names)
    logging.info(results_dict)
    contact_push_callback_log = upload_contact_to_salesforce(results_dict)

    cur.close()


######################################################
# DAG setup
######################################################

dag = DAG(
    "user_contact_sf",
    schedule_interval="@daily",
    default_args=default_args,
    start_date=datetime(2021, 11, 1),
)

push_to_sf = PythonOperator(
    task_id="push_to_sf_usage",
    python_callable=run_sf_push,
    provide_context=True,
    op_kwargs={"main_sql": query_string, "execution_date": "{{ ds }}"},
    dag=dag,
)

push_to_sf
