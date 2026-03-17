from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from src.extract import get_currency_data
from src.transform import transform_currency
from src.load import load_to_clickhouse

def process(start_date, end_date):

    df = get_currency_data(start_date, end_date)

    data = transform_currency(df)

    load_to_clickhouse(data)

with DAG(
    dag_id = 'load_to_clickhouse',
    start_date = datetime(2026,1,1),
    schedule=None,
    catchup=False
) as dag:
    
    task = PythonOperator(
        task_id='load_history',
        python_callable=process,
        op_kwargs={
            'start_date': '2026-01-01',
            'end_date': '2026-02-01'
        }
    )