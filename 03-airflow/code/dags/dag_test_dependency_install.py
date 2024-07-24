from datetime import datetime, timedelta

from airflow.operators.python import PythonOperator
from airflow import DAG

default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def get_pandas():
    import pandas
    print(f"pandas version: {pandas.__version__}")
    
with DAG(
    default_args=default_args,
    dag_id='dag_test_dependency_install',
    start_date=datetime(2024, 7, 22),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='get_pandas',
        python_callable=get_pandas
    )
    
    task1