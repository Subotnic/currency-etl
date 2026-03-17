from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from src.extract import get_currency_data
from src.transform import transform_currency
from src.load import load_to_clickhouse


def extract_task(**context):

    yesterday = datetime.today() - timedelta(days=1)

    date = yesterday.strftime("%Y-%m-%d")

    df = get_currency_data(date, date)

    return df.to_dict()


def transform_task(**context):

    df_dict = context["ti"].xcom_pull(task_ids="extract")

    import pandas as pd
    df = pd.DataFrame(df_dict)

    data = transform_currency(df)

    return data


def load_task(**context):

    data = context["ti"].xcom_pull(task_ids="transform")

    load_to_clickhouse(data)


with DAG(
    dag_id="integration_currency",
    start_date=datetime(2026,1,1),
    schedule="@daily",
    catchup=False
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_task
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_task
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_task
    )

    extract >> transform >> load