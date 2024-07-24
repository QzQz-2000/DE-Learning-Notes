from airflow.decorators import dag, task
from datetime import datetime, timedelta

# create the default args variable to define the retries and retry delay
default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

# create dag using decorator
# in the dag decorator, we will assign values to the parameters
@dag(dag_id='dag_with_taskflow_api_v02',
     default_args=default_args,
     start_date=datetime(2024, 7, 21),
     schedule_interval='@daily')
def hello_world_etl():
    
    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Jerry',
            'last_name': 'Fridman'
        }
    
    @task()
    def get_age():
        return 19
    
    @task()
    def greet(first_name, last_name, age):
        print(f"Hello, my name is {first_name} {last_name} and I am {age} years old!")
       
    name_dict = get_name()
    age = get_age()
    # pass them to the greet function
    greet(first_name=name_dict['first_name'], 
          last_name=name_dict['last_name'], 
          age=age)
  
# the final step to create an instance of our dag   
greet_dag = hello_world_etl()
    