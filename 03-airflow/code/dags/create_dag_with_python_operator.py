from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

# define a single function we want to run as a task
# and we set some parameters
def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f"Hello world! My name is {first_name} {last_name}, and I am {age} years old")
    
# add the task instance
def get_name(ti):
    ti.xcom_push(key='first_name', value='Jerry')
    ti.xcom_push(key='last_name', value='Fridman')

# push the age parameter
def get_age(ti):
    ti.xcom_push(key='age', value='23')

with DAG (
    default_args=default_args,
    dag_id = 'our_dag_with_python_operator_v06',
    description='Our first dag using python operator',
    start_date=datetime(2024,7,20),
    schedule_interval='@daily',     
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        # we annotate the op_kwargs here since we pass the parameters through xcom
        # op_kwargs={'age': 23}
    )
    
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )
    
    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )
    
    [task2, task3] >> task1