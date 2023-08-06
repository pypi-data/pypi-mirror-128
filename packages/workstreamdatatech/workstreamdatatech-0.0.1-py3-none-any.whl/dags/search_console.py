import pandas as pd
from datetime import datetime
from datetime import date, timedelta
import httplib2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from googleapiclient.discovery import build
from collections import defaultdict
from dateutil import relativedelta
import argparse
from oauth2client import file, tools, client
from oauth2client.client import OAuth2WebServerFlow
import re
from dag_configs.config import default_args
import os
from urllib.parse import urlparse

pg_hook = PostgresHook(postgres_conn_id="postgres_db")

"""
Source code:
https://www.jcchouinard.com/get-all-keywords-with-search-console-api/

The following program queries google search console api, and puts data into our database

"""

dag_params = {
    "dag_id": "search_console",
    "start_date": datetime(2020, 9, 30),
    "schedule_interval": "@daily",
}

# Get Domain Name to Create a Project
def get_domain_name(start_url):
    domain_name = "{uri.netloc}".format(
        uri=urlparse(start_url)
    )  # Get Domain Name To Name Project
    domain_name = domain_name.replace(".", "_")
    return domain_name


# Create a project Directory for this website
# def create_project(directory):
#     if not os.path.exists(directory):
#         print('Create project: '+ directory)
#         os.makedirs(directory)


def authorize_creds():
    # Variable parameter that controls the set of resources that the access token permits.
    # SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

    # Path to client_secrets.json file
    # CLIENT_SECRETS_PATH = creds

    # Create a parser to be able to open browser for Authorization
    #     parser = argparse.ArgumentParser(
    #         formatter_class=argparse.RawDescriptionHelpFormatter,
    #         parents=[tools.argparser])
    #     flags = parser.parse_args([])

    #     flow = client.flow_from_clientsecrets(
    #         CLIENT_SECRETS_PATH, scope = SCOPES,
    #         message = tools.message_if_missing(CLIENT_SECRETS_PATH))

    # Prepare credentials and authorize HTTP
    # If they exist, get them from the storage object
    # credentials will get written back to a file.
    storage = file.Storage(
        "/home/ubuntu/workspace/airflow-ecs/dags/credentials/authorizedcreds2.dat"
    )
    credentials = storage.get()

    # If authenticated credentials don't exist, open Browser to authenticate
    #     if credentials is None or credentials.invalid:
    #         credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())
    webmasters_service = build("webmasters", "v3", http=http)
    return webmasters_service


# Create Function to execute your API Request
def execute_request(service, property_uri, request):
    return service.searchanalytics().query(siteUrl=property_uri, body=request).execute()


# Create function to write to CSV
def write_to_csv(data, filename):
    if not os.path.isfile(filename):
        data.to_csv(filename)
    else:  # else it exists so append without writing the header
        data.to_csv(filename, mode="a", header=False)


# Read CSV if it exists to find dates that have already been processed.
def get_dates_from_csv(path):
    if os.path.isfile(path):
        data = pd.read_csv(path)
        data = pd.Series(data["date"].unique())
        return data
    else:
        pass


# Create function to extract all the data
def extract_data(site, num_days, dimensions_array, execution_date):
    # domain_name = get_domain_name(site)
    #     full_path = domain_name + '/' + output
    #     current_dates = get_dates_from_csv(full_path)

    webmasters_service = authorize_creds()

    # Set up Dates
    end_date = datetime.strptime(execution_date, "%Y-%m-%d")
    start_date = end_date - relativedelta.relativedelta(days=num_days)
    delta = timedelta(days=1)  # This will let us loop one day at the time
    scDict = defaultdict(list)
    all_results = []

    while start_date <= end_date:
        #         if current_dates is not None and current_dates.str.contains(datetime.datetime.strftime(start_date,'%Y-%m-%d')).any():
        #             print('Existing Date: %s' % start_date)
        #             start_date += delta
        #         else:
        print("Start date at beginning: %s" % start_date)

        maxRows = 25000  # Maximum 25K per call
        numRows = 0  # Start at Row Zero
        status = ""  # Initialize status of extraction

        while (
            status != "Finished"
        ):  # Test with i < 10 just to see how long the task will take to process.
            request = {
                "startDate": datetime.strftime(start_date, "%Y-%m-%d"),
                "endDate": datetime.strftime(start_date, "%Y-%m-%d"),
                "dimensions": dimensions_array,
                "rowLimit": maxRows,
                "startRow": numRows,
            }

            response = execute_request(webmasters_service, site, request)

            try:
                # Process the response
                for row in response["rows"]:
                    for i in range(len(row["keys"])):
                        scDict[dimensions_array[i]].append(row["keys"][i] or 0)
                    scDict["clicks"].append(row["clicks"] or 0)
                    scDict["ctr"].append(row["ctr"] or 0)
                    scDict["impressions"].append(row["impressions"] or 0)
                    scDict["position"].append(row["position"] or 0)
                print("successful at %i" % numRows)

            except:
                print("error occurred at %i" % numRows)

            # Add response to dataframe
            df = pd.DataFrame(data=scDict)
            df["clicks"] = df["clicks"].astype("int")
            df["ctr"] = df["ctr"] * 100
            df["impressions"] = df["impressions"].astype("int")
            df["position"] = df["position"].round(2)
            df_result = df.to_dict(orient="records")

            print("Numrows at the start of loop: %i" % numRows)
            try:
                numRows = numRows + len(response["rows"])
            except:
                status = "Finished"
            print("Numrows at the end of loop: %i" % numRows)
            if numRows % maxRows != 0:
                status = "Finished"
            all_results += df_result

        start_date += delta
        print("Start date at end: %s" % start_date)

    return all_results


def upload_to_postgres(input_result, table_name, dimensions_array):

    cur = pg_hook.get_cursor()
    columns_str = ", ".join(["%({var})s".format(var=x) for x in dimensions_array])
    insert_statement = """INSERT INTO {table_name}_temp VALUES \
    ({columns_str},%(clicks)s,%(ctr)s,%(impressions)s,%(position)s);
    commit;
    """.format(
        **{"table_name": table_name, "columns_str": columns_str}
    )
    cur.executemany(insert_statement, input_result)
    cur.close()
    return


def pull_data(**kwargs):

    results = extract_data(
        site=kwargs["site"],
        num_days=kwargs["num_days"],
        dimensions_array=kwargs["dimensions_array"],
        execution_date=kwargs["execution_date"],
    )
    upload_to_postgres(results, kwargs["table_name"], kwargs["dimensions_array"])
    return


def latest_record(**kwargs):

    cur = pg_hook.get_cursor()
    sql_for_latest_record = """
    truncate table {table_name};
    insert into {table_name}
    with latest_record_rn as (
    SELECT *
         , row_number() over (partition by {dimensions_partition} order by insert_ts desc) rn
    FROM {table_name}_temp
    )
    select 
        {dimensions_partition}
        , clicks
        , ctr
        , impressions
        , position
        , insert_ts
    from latest_record_rn
    where rn = 1;
    commit;
    """.format(
        **{
            "dimensions_partition": ", ".join(kwargs["dimensions_partition"]),
            "table_name": kwargs["table_name"],
        }
    )
    cur.execute(sql_for_latest_record)
    cur.close()
    return


dag = DAG("search_console", default_args=default_args, schedule_interval="@daily")

site = "https://www.workstream.us"
num_days = 2
dimensions_array_page_overall = ["date", "page"]
dimensions_array_page = ["date", "page", "country", "device"]
dimensions_array_page_query = ["date", "page", "query", "country", "device"]

pull_from_console_to_db_pages = PythonOperator(
    task_id="pull_pages_from_console_to_db",
    python_callable=pull_data,
    op_kwargs={
        "site": site,
        "num_days": num_days,
        "dimensions_array": dimensions_array_page,
        "execution_date": "{{ ds }}",
        "table_name": "search_console.page_metrics",
    },
    provide_context=True,
    dag=dag,
)

pull_from_console_to_db_pages_overall = PythonOperator(
    task_id="pull_pages_overall_from_console_to_db",
    python_callable=pull_data,
    op_kwargs={
        "site": site,
        "num_days": num_days,
        "dimensions_array": dimensions_array_page_overall,
        "execution_date": "{{ ds }}",
        "table_name": "search_console.page_overall_metrics",
    },
    provide_context=True,
    dag=dag,
)

pull_from_console_to_db_pages_query = PythonOperator(
    task_id="pull_pages_query_from_console_to_db",
    python_callable=pull_data,
    op_kwargs={
        "site": site,
        "num_days": num_days,
        "dimensions_array": dimensions_array_page_query,
        "execution_date": "{{ ds }}",
        "table_name": "search_console.page_query_metrics",
    },
    provide_context=True,
    dag=dag,
)

create_view_latest_record_pages = PythonOperator(
    task_id="create_view_latest_record_pages",
    python_callable=latest_record,
    op_kwargs={
        "dimensions_partition": dimensions_array_page,
        "table_name": "search_console.page_metrics",
    },
    provide_context=True,
    dag=dag,
)

create_view_latest_record_pages_query = PythonOperator(
    task_id="create_view_latest_record_query",
    python_callable=latest_record,
    op_kwargs={
        "dimensions_partition": dimensions_array_page_overall,
        "table_name": "search_console.page_overall_metrics",
    },
    provide_context=True,
    dag=dag,
)

create_view_latest_record_pages_overall = PythonOperator(
    task_id="create_view_latest_record_pages_overall",
    python_callable=latest_record,
    op_kwargs={
        "dimensions_partition": dimensions_array_page_query,
        "table_name": "search_console.page_query_metrics",
    },
    provide_context=True,
    dag=dag,
)


pull_from_console_to_db_pages >> create_view_latest_record_pages
pull_from_console_to_db_pages_query >> create_view_latest_record_pages
pull_from_console_to_db_pages_overall >> create_view_latest_record_pages
create_view_latest_record_pages >> create_view_latest_record_pages_query
create_view_latest_record_pages_query >> create_view_latest_record_pages_overall
