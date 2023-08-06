from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd
import boto3
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from dag_configs.config import default_args
from airflow import DAG

coa_rename_dict = {
    "Account #": "account_no",
    "Account": "account",
    "Type": "account_type",
    "Detail type": "detail_type",
    "Description": "description",
    "Balance": "balance",
    "Currency": "currency",
}

transactions_rename_dict = {
    "Date": "date",
    "Transaction Type": "transaction_type",
    "Name": "transaction_name",
    "Memo/Description": "memo_description",
    "Account": "account_name_original",
    "Split": "split",
    "Amount": "amount",
    "Class": "class",
    "Vendor": "vendor",
}

unaccepted_account_names = [
    "20000 Brex",
    "10000 Checking-First Republic",
    "10010 Checking-Silicon Valley",
]
final_columns = [
    "date",
    "transaction_type",
    "transaction_name_edit",
    "memo_description",
    "account_name_original",
    "split",
    "amount",
    "class",
    "account_name_edit",
    "account_no",
    "account_name",
    "account_type",
]


def rename_coa_df(coa):
    # All preprocessing for chart of accounts
    coa = coa.rename(columns=coa_rename_dict)
    coa = coa.drop("Unnamed: 0", axis=1)
    print("cols from coa file", coa.columns)
    coa = coa[~coa["account_no"].isnull()]
    coa["account_no"] = coa["account_no"].astype(int)
    return coa


def rename_transactions_df(df):
    df = df.drop("Unnamed: 0", axis=1)
    df = df.rename(columns=transactions_rename_dict)
    df["account_name_edit"] = df.apply(
        lambda x: x["split"]
        if x["account_name_original"] in unaccepted_account_names
        else x["account_name_original"],
        1,
    )
    df = df[~df["date"].isnull()]
    return df


def preprocess_transactions(df, coa):
    df["transaction_name_edit"] = df["transaction_name"].fillna(df["vendor"])
    # filter out null date rows
    df["date"] = pd.to_datetime(df["date"])
    df["account_no"] = df["account_name_edit"].apply(lambda x: x.split(" ")[0])
    df["account_name"] = df["account_name_edit"].apply(
        lambda x: " ".join(x.split(" ")[1:])
    )
    df["amount"] = df["amount"].apply(
        lambda x: float(x.replace(" ", "").replace(",", "")), 1
    )
    #     df = df.drop(['Unnamed: 0','Num'],axis=1)
    df_merged = df.merge(
        coa[["account", "account_type"]], left_on="account_name", right_on="account"
    )
    df_merged = df_merged[final_columns]
    return df_merged


def write_df_to_table(table_name, df):
    records = df.to_dict(orient="records")
    columns = df.columns
    col_str = ",".join(["%(" + x + ")s" for x in columns])
    full_str = "INSERT INTO {table_name} VALUES (" + col_str + "); commit;"
    insert_statement = full_str.format(**{"table_name": table_name})
    print(insert_statement)

    pg_hook = PostgresHook(postgres_conn_id="postgres_db")
    cur = pg_hook.get_cursor()
    cur.executemany(insert_statement, records)


def run_ingest_quickbooks(**kwargs):
    ACCESS_KEY = Variable.get("QUICKBOOKS_ACCESS_KEY")
    SECRET_KEY = Variable.get("QUICKBOOKS_SECRET_KEY")

    bucket = "quickbooksdatamirae"
    transactions_file_name = "transactions/2021-10-11_transactions.csv"
    coa_file_name = "chart_of_accounts/2021-10-11_chart_of_accounts.csv"

    s3 = boto3.client(
        "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
    )

    obj_transactions = s3.get_object(Bucket=bucket, Key=transactions_file_name)
    obj_coa = s3.get_object(Bucket=bucket, Key=coa_file_name)

    raw_transactions_df = pd.read_csv(obj_transactions["Body"], header=4)
    raw_coa_df = pd.read_csv(obj_coa["Body"], header=4)
    print(raw_transactions_df.head())
    print(raw_coa_df.head())

    coa_df = rename_coa_df(raw_coa_df)
    print("finished_coa_file")
    transactions_df = rename_transactions_df(raw_transactions_df)
    print("finished transactions file")
    final_df = preprocess_transactions(transactions_df, coa_df)
    final_df["run_time"] = datetime.now().isoformat()
    print("start", final_df.columns)
    write_df_to_table("quickbooks.transactions", final_df)
    print("done")


with DAG("quickbooks_ingestion", max_active_runs=3, default_args=default_args) as dag:

    ingest_qb = PythonOperator(
        task_id="ingest_quickbooks",
        python_callable=run_ingest_quickbooks,
        provide_context=True,
        op_kwargs={"execution_time": "{{ ts }}", "run_id": "{{ run_id}}"},
    )

    dummy_task = DummyOperator(task_id="test")

    run_sql = PostgresOperator(
        postgres_conn_id="postgres_db",
        task_id="run_quickbooks_view_sql",
        sql="sql/quickbooks_transactions_edit.sql",
    )

    ingest_qb >> dummy_task
    dummy_task >> run_sql
