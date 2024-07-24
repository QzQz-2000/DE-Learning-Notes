# a dag implementation is an instantiation of the class DAG, 
# therefore we have to firstly import DAG
from airflow import DAG
# determine the start time, import timedelta to set the retry time
from datetime import datetime, timedelta
# we will use BashOperator
from airflow.operators.bash import BashOperator

# define the common parameters to initialise the operator in default_args
default_args = {
    'owner': 'Bowen',
    'retries': 5,
    # The retry interval after a task failure is 2 minutes
    'retry_delay': timedelta(minutes=2)  
}

# create an instance of DAG using the `with` statement
with DAG(
    dag_id='our_first_dag',
    default_args=default_args,
    description='This is our first dag',
    # 2024/07/20/2am
    start_date=datetime(2024,7,20,2),
    schedule_interval='@daily'
) as dag:
    # create first task
    task1 = BashOperator(
        task_id = 'first_task',
        bash_command='echo hello world'
    )
    
    task1