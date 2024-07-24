from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_postgres_operator_v02',
    default_args=default_args,
    start_date=datetime(2024, 7,22),
    schedule_interval='@daily'
) as dag:
    task1 = PostgresOperator(
        task_id='create_postgres_table',
        # the connection id of the connection
        postgres_conn_id='postgres_localhost',
        # create a table
        sql="""
            create table if not exists dag_runs (
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            ) 
        """
    )
    
    task2 = PostgresOperator(
        task_id='delete_data_from_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            delete from dag_runs where dt = '{{ ds }}' and dag_id = '{{ dag.dag_id }}'
        """
    )
    
    task3 = PostgresOperator(
        task_id='insert_into_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            insert into dag_runs (dt, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}')
        """
    )
    
    task1 >> task2 >> task3