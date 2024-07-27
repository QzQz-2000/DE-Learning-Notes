[TOC]

## Common ETL pain points (on-call)

### Key Points

- Increasing data volume
- Quickly troubleshooting task failures
- Each new tool requires learning new standards
- Retry, monitoring, and alerting
- Agile and efficient development to meet business needs
- Uneven data peaks

### Airflow Design Philosophy

- **Dynamic**: Airflow pipelines are defined as code (Python), allowing for dynamic pipeline generation. This allows for writing code to dynamically instantiate pipelines.
- **Scalable**: Easily define your own operators, executors, and extension libraries, making them suitable for the level of abstraction of the environment.
- **Elegant**: Airflow pipelines are simple and clear, using the powerful Jinja template engine to parametrize script parameters built into Airflow’s core.
- **Modular Architecture**: Airflow has a modular architecture and uses message queues to coordinate an arbitrary number of workers, making it scalable to infinity.

### Components

- **Scheduler**
  - The Scheduler is a process that uses DAG definitions combined with metadata to determine which tasks need to be executed and their execution priorities. The Scheduler typically runs as a service.
  - The Scheduler starts a subprocess to monitor all DAGs, generally collecting DAG changes and executing them every minute.
  - It has three steps:
    - Check all DAGs that need a new DagRun and create them.
    - Examine a batch of DagRuns for schedulable TaskInstances or complete DagRuns.
    - Select schedulable TaskInstances, and while respecting Pooling limits and other concurrency limits, enqueue them for execution.

- **WebServer**
  - Provides a graphical interface to monitor DAG run status and perform operations on DAGs. The WebServer uses the Gunicorn framework.

- **Metadata Database**
  - The metadata database, which defaults to SQLite, can also support MySQL and PostgreSQL. It stores all DAGs, task definitions, run history, users, permissions, etc.

- **Worker**
  - Used to execute tasks received by the Executor, these are the processes that actually execute the task logic, determined by the executor in use.

![2](./images/2.png)

- Webserver会从metadata database中读取相应的用户配置、状态等。
- Scheduler会定期扫描DAG文件夹，处理新增、修改的DAG数据。
- Executor是Scheduler的一部分，起到trigger worker工作的作用。

Airflow兼容多种组件，最关键的executor有四种选择：

- SequentialExecutor：单进程顺序执行任务，默认执行器，运行速度很慢，通常只用于测试
- LocalExecutor：多进程本地执行任务
- CeleryExecutor：分布式调度，生产常用
- DaskExecutor：动态任务调度，主要用于数据分析

## Run Airflow in Docker

First fetch the yaml file:

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.3/docker-compose.yaml'
```

We run airflow in docker, and we make some changes in the yaml file. Following is the final version of the yaml file.

```yaml
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

# Basic Airflow cluster configuration for CeleryExecutor with Redis and PostgreSQL.
#
# WARNING: This configuration is for local development. Do not use it in a production deployment.
#
# This configuration supports basic configuration using environment variables or an .env file
# The following variables are supported:
#
# AIRFLOW_IMAGE_NAME           - Docker image name used to run Airflow.
#                                Default: apache/airflow:2.9.3
# AIRFLOW_UID                  - User ID in Airflow containers
#                                Default: 50000
# AIRFLOW_PROJ_DIR             - Base path to which all the files will be volumed.
#                                Default: .
# Those configurations are useful mostly in case of standalone testing/running Airflow in test/try-out mode
#
# _AIRFLOW_WWW_USER_USERNAME   - Username for the administrator account (if requested).
#                                Default: airflow
# _AIRFLOW_WWW_USER_PASSWORD   - Password for the administrator account (if requested).
#                                Default: airflow
# _PIP_ADDITIONAL_REQUIREMENTS - Additional PIP requirements to add when starting all containers.
#                                Use this option ONLY for quick checks. Installing requirements at container
#                                startup is done EVERY TIME the service is started.
#                                A better way is to build a custom image or extend the official image
#                                as described in https://airflow.apache.org/docs/docker-stack/build.html.
#                                Default: ''
#
# Feel free to modify this file to suit your needs.
---
x-airflow-common:
  &airflow-common
  # In order to add custom dependencies or upgrade provider packages you can use your extended image.
  # Comment the image line, place your Dockerfile in the directory where you placed the docker-compose.yaml
  # and uncomment the "build" line below, Then run `docker-compose build` to build the images.
  image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.9.3}
  # build: .
  environment:
    &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: LocalExecutor
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CORE__FERNET_KEY: ''
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
    AIRFLOW__CORE__LOAD_EXAMPLES: 'true'
    AIRFLOW__API__AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session'
    # yamllint disable rule:line-length
    # Use simple http server on scheduler for health checks
    # See https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/check-health.html#scheduler-health-check-server
    # yamllint enable rule:line-length
    AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK: 'true'
    # WARNING: Use _PIP_ADDITIONAL_REQUIREMENTS option ONLY for a quick checks
    # for other purpose (development, test and especially production usage) build/extend Airflow image.
    _PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-}
    # The following line can be used to set a custom config file, stored in the local config folder
    # If you want to use it, outcomment it and replace airflow.cfg with the name of your config file
    # AIRFLOW_CONFIG: '/opt/airflow/config/airflow.cfg'
  volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
  user: "${AIRFLOW_UID:-50000}:0"
  depends_on:
    &airflow-common-depends-on
    postgres:
      condition: service_healthy

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 10s
      retries: 5
      start_period: 5s
    restart: always

  airflow-webserver:
    <<: *airflow-common
    command: webserver
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-scheduler:
    <<: *airflow-common
    command: scheduler
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8974/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on

  airflow-triggerer:
    <<: *airflow-common
    command: triggerer
    healthcheck:
      test: ["CMD-SHELL", 'airflow jobs check --job-type TriggererJob --hostname "$${HOSTNAME}"']
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-init:
    <<: *airflow-common
    entrypoint: /bin/bash
    # yamllint disable rule:line-length
    command:
      - -c
      - |
        if [[ -z "${AIRFLOW_UID}" ]]; then
          echo
          echo -e "\033[1;33mWARNING!!!: AIRFLOW_UID not set!\e[0m"
          echo "If you are on Linux, you SHOULD follow the instructions below to set "
          echo "AIRFLOW_UID environment variable, otherwise files will be owned by root."
          echo "For other operating systems you can get rid of the warning with manually created .env file:"
          echo "    See: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user"
          echo
        fi
        one_meg=1048576
        mem_available=$$(($$(getconf _PHYS_PAGES) * $$(getconf PAGE_SIZE) / one_meg))
        cpus_available=$$(grep -cE 'cpu[0-9]+' /proc/stat)
        disk_available=$$(df / | tail -1 | awk '{print $$4}')
        warning_resources="false"
        if (( mem_available < 4000 )) ; then
          echo
          echo -e "\033[1;33mWARNING!!!: Not enough memory available for Docker.\e[0m"
          echo "At least 4GB of memory required. You have $$(numfmt --to iec $$((mem_available * one_meg)))"
          echo
          warning_resources="true"
        fi
        if (( cpus_available < 2 )); then
          echo
          echo -e "\033[1;33mWARNING!!!: Not enough CPUS available for Docker.\e[0m"
          echo "At least 2 CPUs recommended. You have $${cpus_available}"
          echo
          warning_resources="true"
        fi
        if (( disk_available < one_meg * 10 )); then
          echo
          echo -e "\033[1;33mWARNING!!!: Not enough Disk space available for Docker.\e[0m"
          echo "At least 10 GBs recommended. You have $$(numfmt --to iec $$((disk_available * 1024 )))"
          echo
          warning_resources="true"
        fi
        if [[ $${warning_resources} == "true" ]]; then
          echo
          echo -e "\033[1;33mWARNING!!!: You have not enough resources to run Airflow (see above)!\e[0m"
          echo "Please follow the instructions to increase amount of resources available:"
          echo "   https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#before-you-begin"
          echo
        fi
        mkdir -p /sources/logs /sources/dags /sources/plugins
        chown -R "${AIRFLOW_UID}:0" /sources/{logs,dags,plugins}
        exec /entrypoint airflow version
    # yamllint enable rule:line-length
    environment:
      <<: *airflow-common-env
      _AIRFLOW_DB_MIGRATE: 'true'
      _AIRFLOW_WWW_USER_CREATE: 'true'
      _AIRFLOW_WWW_USER_USERNAME: ${_AIRFLOW_WWW_USER_USERNAME:-airflow}
      _AIRFLOW_WWW_USER_PASSWORD: ${_AIRFLOW_WWW_USER_PASSWORD:-airflow}
      _PIP_ADDITIONAL_REQUIREMENTS: ''
    user: "0:0"
    volumes:
      - ${AIRFLOW_PROJ_DIR:-.}:/sources

  airflow-cli:
    <<: *airflow-common
    profiles:
      - debug
    environment:
      <<: *airflow-common-env
      CONNECTION_CHECK_MAX_COUNT: "0"
    # Workaround for entrypoint issue. See: https://github.com/apache/airflow/issues/16252
    command:
      - bash
      - -c
      - airflow
      
volumes:
  postgres-db-volume:
```

Now we need to create folders for dags, logs and plugins.

```bash
mkdir -p ./dags ./logs ./plugins ./config
```

Now run the database migrations and create the first user account.

```bash
docker compose up airflow-init
```

The account created has the login `airflow` and the password `airflow`. Start all services:

```bash
docker compose up -d
```

### Core concepts

#### Workflow

Workflow is a sequence of tasks. In airflow, workflow is defined as DAG, namely directed acyclic graph which cannot contain cycles.

#### Task

A task defines as a unit of work within a DAG. It's represented as a node in the DAG and is written in Python. And there is a dependency between tasks.

#### Operators

The method it uses is called operator. DAGs describe how to run a workflow. Operators determine what actually gets done by a task. Each task is an implementation of an operator. An operator determines what to be done and a task implements an operator by defining specific values for that operator.

- BashOperator
- PythonOperator
- Customised Operator

#### Property

- Execution Date: logical date and time which the DAG Run
- Task Instance: a run of a task at a specific point of time (execution_date)
- Dag Run: an instantiation of a DAG, containing task instances that run for a specific execution_date.

![5](./images/5.png)

### Task lifecycle

phase 1:

- no_status: scheduler created empty task instance

phase 2:

- scheduled: scheduler determined task instance needs to be run
- removed:
- upstream failed: the task's upstream task failed
- skipped: task is skipped

phase 3:

- queued: if the task is scheduled, the executor will put the task into the task queue

phase 4:

- running: worker picked up a task and is now running it

phase 5:

- success: task completed without error
- failed: task failed
- shutdown: task run has been shutdown
- up_for_reschedule: task will be rescheduled every certain time interval

phase 6:

up_for_retry: In the case of the task in stages failed or shutdown, if the maximum retry is not exceeded, the task will be forward to up for retry stage, which means the task will be scheduled and rerun after a certain waiting time.

![6](./images/6.png)

### Basic Architecture

![7](./images/7.png)

- Data engineer: build and monitor all the ETL process. 
  - Configure the airflow setup in `Airflow.cfg`:
    - the type the executor
    - the database to use
  - create and manage DAGs through the airflow user interface (Web Server)
- Web Server:  create and manage the tasks
- Scheduler: schedule the tasks (change the task's status during the whole lifecycle)
- Workers: run the tasks (change the task's status during the whole lifecycle)
- Executor: execute the tasks
- Database: various database engines you can choose, like mysql, postgres.

In order to persist the update and retrieve the info of the DAGs, those four components are connected to the database closely.

## Create our own DAGs

There are several steps when creating an new DAG:

- import required packages
- set `default_args`
  - owner
  - retries
  - retry_delay
- create a DAG instance
- initialize the DAG by setting required parameters
  - dag_id
  - default_args
  - start_date
  - schedule_interval
- create tasks
- manage the dependencies between the tasks

```bash
# shut down the containers, '-v' means removing the volumes we defined in our yaml file
docker compose down -v

# change this to false to remove the example DAGs
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'

# init the airflow
docker compose up airflow-init

# launch the services up
docker compose up -d
```

### First DAG (BashOperator)

Let's create our first DAG under the `dags` directory named `our_first_dag.py`:

```bash
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
    # # The retry interval after a task failure is 2 minutes
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
```

Then go to the web ui to trigger the task. In the log you can see the output:

![8](./images/8.png)

### Second DAG (BashOperator)

In general, an ETL process consists of multiple tasks. To set the dependencies of tasks, we have several methods.

```python
# first method
task1.set_downstream(task2)
task1.set_downstream(task3)

# second method
task1 >> task2
task1 >> task3

# third method (adjusted version of the second method)
task1 >> [task2, task3]
```

```python
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
    dag_id='our_second_dag',
    default_args=default_args,
    description='This is our first dag',
    # 2024/07/20/2am
    start_date=datetime(2024,7,20,2),
    schedule_interval='@daily'
) as dag:
    # create first task
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo hello world, this is our first task'
    )
    
    task2 = BashOperator(
        task_id='second_task',
        bash_command='echo hey, i am task 2'  
    )
    
    task3 = BashOperator(
        task_id='third_task',
        bash_command='echo hey, i am task 3'
    )
    
    # task1.set_downstream(task2)
    # task1.set_downstream(task3)
    
    # task1 >> task2
    # task1 >> task3
    
    task1 >> [task2, task3]
```

### PythonOperator DAG

Here we define a python function to be run as a task, and also pass some parameters using `op_kwargs`.

```python
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
def greet(name, age):
    print(f"Hello world! My name is {name}, and I am {age} years old")

with DAG (
    default_args=default_args,
    dag_id = 'our_dag_with_python_operator_v01',
    description='Our first dag using python operator',
    start_date=datetime(2024,7,20),
    schedule='@daily',     
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        # a dictionary of keyword arguments that will get unpacked in the python function
        op_kwargs={'name': 'Bowen', 'age': 23}
    )
    
    task1
```

## Xcoms

We can share information between tasks using `xcoms`. Basically we can push info to `xcoms` in one task and pull info in other tasks. By default, every function's return value will be automatically pushed into `xcom`. Now we change the DAG to the following:

```python
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
def greet(name, age):
    print(f"Hello world! My name is {name}, and I am {age} years old")
    
def get_name():
    return "Bowen"

with DAG (
    default_args=default_args,
    dag_id = 'our_dag_with_python_operator_v02',
    description='Our first dag using python operator',
    start_date=datetime(2024,7,20),
    schedule='@daily',     
) as dag:
    # task1 = PythonOperator(
    #     task_id='greet',
    #     python_callable=greet,
    #     # a dictionary of keyword arguments that will get unpacked in the python function
    #     op_kwargs={'name': 'Bowen', 'age': 23}
    # )
    
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name,
    )
    
    task2
```

Trigger and run the DAG, we can see the log output:

<img src="./images/9.png" alt="9"  />

Go to the `Admin` and click the `xcom` tab, we can see the return value of the python function.

![10](./images/10.png)

Now let's add a task instance named `ti` since `xcom-pull` can only be called by `ti`. Let's pull the name of "Jerry".

```python
# remove the 'name' parameter and get 'name' from the return value
def greet(age, ti):
    name = ti.xcoms_pull(task_ids='get_name')
    print(f"Hello world! My name is {name}, and I am {age} years old")
    
# delete the 'name' parameter
op_kwargs={'age': 23}

# build the dependency, task2 is the downstream of task1, since task1 needs the return value of task 2
task2 >> task1
```

The complete code is as follows:

```python
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
def greet(age, ti):
    name = ti.xcom_pull(task_ids='get_name')
    print(f"Hello world! My name is {name}, and I am {age} years old")
    
def get_name():
    return "Jerry"

with DAG (
    default_args=default_args,
    dag_id = 'our_dag_with_python_operator_v03',
    description='Our first dag using python operator',
    start_date=datetime(2024,7,20),
    schedule='@daily',     
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        # a dictionary of keyword arguments that will get unpacked in the python function
        op_kwargs={'age': 23}
    )
    
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name,
    )
    
    task2 >> task1
```

Now we can see the output. 

![11](./images/11.png)

Now we want to push multiple values into xcoms in one function.

```python
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
def greet(age, ti):
    first_name = ti.xcom_pull(task_id='get_name', key='first_name')
    last_name = ti.xcom_pull(task_id='get_name', key='last_name')
    print(f"Hello world! My name is {first_name} {last_name}, and I am {age} years old")
    
# add the task instance
def get_name(ti):
    ti.xcom_push(key='first_name', value='Jerry')
    ti.xcom_push(key='last_name', value='Fridman')
    

with DAG (
    default_args=default_args,
    dag_id = 'our_dag_with_python_operator_v04',
    description='Our first dag using python operator',
    start_date=datetime(2024,7,20),
    schedule='@daily',     
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        # a dictionary of keyword arguments that will get unpacked in the python function
        op_kwargs={'age': 23}
    )
    
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name,
    )
    
    task2 >> task1
```

![12](./images/12.png)

> Tip: notice that `xcom_pull` use parameter `task_ids`, not `task_id`.

We can do a similar operation to `age` parameter.

```python
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
```

![13](./images/13.png)

Although it's very handy to use `xcom` to share values between tasks, you should be aware that the maximum size of `xcom` is only 48 kb. So never use `xcom` to share large data for example pandas dataframe, otherwise it will crash.

## TaskFlow

We can reduce the code size by rewriting it using the `TaskFlow`. Let's create a python file named `dag_with_taskflow_api.py`.

Each task is represented by a python function with the task decorator. The `TaskFlow` API automatically calculate the dependency. What we need to do is to call the `get_name` and `get_age` function to get the returned variables.

![14](./images/14.png)

If we want to pass multiple parameters, we should set the `multiple_outputs` parameter to `True`.

```python
@task(multiple_outputs=True)
def get_name():
    return {
        'first_name': 'Jerry',
        'last_name': 'Fridman'
    }
```

```python
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
```

Let's look at `xcom`. Here we can see the return value.

![15](./images/15.png)

### Dag with catchup and backfill

Let's go back to vscode and create a new dag called `dag_with_catchup_and_backfill.py`. There is a parameter called `catchup`.

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_catchup_and_backfill_v01',
    default_args=default_args,
  # today is 2024/07021
    start_date=datetime(2024,7,10),
    schedule_interval='@daily',
    catchup=True
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo This is a simple bash command!'
    )
```

The `catchup` feature helps us run the dag since the start time. The main function of the `catchup` parameter is to control whether the DAG should backfill and execute previously missed task instances at startup.

- **catchup=True**: When `catchup` is set to `True`, Airflow will attempt to run all task instances from the DAG's start date (`start_date`) to the current date. If your DAG has a `start_date` set to a past date and is scheduled to run periodically, Airflow will execute every scheduled run until it catches up to the current date.

- **catchup=False**: When `catchup` is set to `False`, Airflow will only execute tasks starting from the current time and will not backfill past task instances. This is particularly useful for DAGs that do not need to process historical data.

Now set the `catchup` to `False`. We can use backfill 

```bash
docker ps

# open its bash interactively in the container
docker exec -it <container-id> bash

# use the command with start date (like '2024-07-01'), end date and the dag id
airflow dags backfill -s <start date> -e <end date>

# here we have
airflow@b8647d758ea8:/opt/airflow$ airflow dags backfill -s 2024-07-01 -e 2024-07-12 dag_with_catchup_and_backfill_v02

# exit the container
exit
```

We can see the log:

```
...
[2024-07-21T22:18:47.063+0000] {dagrun.py:704} INFO - DagRun Finished: dag_id=dag_with_catchup_and_backfill_v02, execution_date=2024-07-08T00:00:00+00:00, run_id=backfill__2024-07-08T00:00:00+00:00, run_start_date=2024-07-21 22:18:27.515482+00:00, run_end_date=2024-07-21 22:18:47.062696+00:00, run_duration=19.547214, state=success, external_trigger=False, run_type=backfill, data_interval_start=2024-07-08T00:00:00+00:00, data_interval_end=2024-07-09T00:00:00+00:00, dag_hash=None
[2024-07-21T22:18:47.076+0000] {dagrun.py:653} INFO - Marking run <DagRun dag_with_catchup_and_backfill_v02 @ 2024-07-10T00:00:00+00:00: backfill__2024-07-10T00:00:00+00:00, state:running, queued_at: None. externally triggered: False> successful
...
```

Go to the browser, we can see the records.

<img src="./images/16.png" alt="16" style="zoom:50%;" />

### Scheduler with Cron Expression

In airflow, creating a dag needs the `schedule_interval` parameter, which receives a cron expression as a string. Cron expression is a string comprising five fields separated by white space that represents a set of times. It's normally as a schedule to execute some routine.

<img src="./images/17.png" alt="17" style="zoom:50%;" />

Airflow already provide some preset:

![18](./images/18.png)

Let's create a new dag file called `dag_with_cron_expression.py`.

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id='dag_with_cron_expression_v01',
    start_date=datetime(2024, 7, 1),
    schedule_interval='0 0 * * *'
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo dag with cron expression!'
    )
    
    task1
```

Here we can see that the cron string `0 0 * * *` serve the same purpose as `@daily`. How to generate customized schedule_interval using the cron expression? We can go to this website: [crontab.guru](https://crontab.guru/). This gives us a visual way to generate and verify the cron expression.

![19](./images/19.png)

For example, here we scheduled the task to be run weekly on Wednesday at 07:40. If we want to run our dag weekly on multiple days, we just need to add a comma.

```bash
# run weekly on wed and fri at 07"40
40 7 * * wed, fri

# run weekly from tue through fri
40 7 * * tue-fri
```

## Airflow Connection

Normally when we build an ETL DAG, we need to connect to some external services. For example:

- Database Servers
  - MySQL
  - Postgresql
- Cloud Servers
  - AWS
  - Azure
- Other services

To connect to these services, we need the `credentials` like:

- host
- user
- password
- ...

We can create and manage them easily by `Airflow Connection`, which can be used by corresponding operators.

![20](./images/20.png)

In the web ui, we can see the `Connection` tab. Click on the `+` button to add a new connection.

![21](./images/21.png)

Here we can see different types of connection that we can create. If the connection type is missing, you can just install the corresponding **provider packages** or create your own **customized connection**.

### Airflow PostgresOperator

Let's learn how to use it with `PostgresOperator`. We need a postgres database. Let's expose the postgres database we use in the airflow project by adding ports in the `yaml` file:

```yaml
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    # expose postgres db
    ports:
      - 5432:5432
```

Then we can recreate the `postgres` container.

```bash
docker-compose up -d --no-deps --build postgres
```

Install `DBeaver` and create a new `PostgreSQL` connection.

![22](./images/22.png)

![23](./images/23.png)

Then click on the `Test Connection` button, then we connected successfully. Once finished, create a new database named `test`. Let's use an airflow dag to create a table and insert some values into the database.

Create a new connection in the web ui.

![24](./images/24.png)

For `Host`, we can either use the name of the services in the `yaml` file which is `postgress` or `host.docker.internal` when we are using docker desktop to connect to localhost from a container.

![25](./images/25.png)

Go back to vscode and create a dag file named `dag_with_postgres_operator.py`.

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_postgres_operator_v01',
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
    
    task1
```

Run the DAG and go to the DBeaver. The table has been created successfully.

<img src="./images/26.png" alt="截屏2024-07-22 17.19.25" style="zoom:50%;" />

Let's create another task which inserts the `dag_id` and `execution date` into the table.

```sql
insert into dag_runs (dt, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}')
```

Here `dt` is the dag run's execution date and the `dag_id` is the dag id, which are set by default by airflow engine and can be accessed by putting the variable into `{{}}`. We can search the [**airflow macro documentation**](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html). 

> Tips: {{}} is Jinja grammar

```python 
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
        task_id='insert_into_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            insert into dag_runs (dt, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}')
        """
    )
    
    task1 >> task2
```

```
[2024-07-22, 17:34:53 CEST] {sql.py:418} INFO - Running statement: 
            insert into dag_runs (dt, dag_id) values ('2024-07-22', 'dag_with_postgres_operator_v02')
        , parameters: None
[2024-07-22, 17:34:53 CEST] {sql.py:427} INFO - Rows affected: 1
```

In airflow, it's recommended to delete data before insert to avoid data duplication or primary key violation. We can do this by adding a delete task before insert.

```python
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
```

![27](./images/27.png)

Now we can see that the record has been successfully inserted into the database.

## Airflow Docker Install Python Package

There are 2 ways to install python dependencies to your airflow docker container.

- Image Extending
  - only need basic knowledge of docker images, it doesn't need the airflow source code
  - build fast
- Image Customising
  - build from the airflow sources
  - can heavily optimize the image size

![28](./images/28.png)

Let's go back to vscode and create the `requirements` text file, in which we can define the python dependencies.

```txt
pandas
```

### Image Extending

Now we are going to install all the dependencies defined in the requirement file by extending the airflow image. To do that, we have to create a `Dockerfile` in our projects root folder.

```dockerfile
# tells docker that we want to extend the offcial docker image with version 2.7.3
FROM apache/airflow:2.7.3

# copy the requirements file to the docker image
COPY requirements.txt /requirements.txt

# run the upgrade command to have the latest pip version
RUN pip install --user --upgrade pip

# run the pip install to get all the python dependencies installed
RUN pip install --no-cache-dir --user -r /requirements.txt
```

Let's build the extended image by command:

```bash
docker build . --tag extending_airflow:latest
```

Basically we tell the docker to build an image using the `Dockerfile` existing in the current directory and name the image as `extending_airflow` and the version as `latest`. Once it finishes, we need to open our docker-compose yaml file to change the image name from `apache/airflow:2.7.3` to `extending_airflow:latest`.

Let's create a dag file to verify whether the `pandas` packages has been installed.

```python
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
```

Save it and we need to rebuild the airflow webserver and scheduler services since we modified the airflow image name in the `yaml` file.

```bash
docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler
```

Go to the browser, login and refresh the page. Trigger our newly created dag and check the log.![29](./images/29.png)

Now we can see that the dependency has been successfully installed.

Whenever we change our python dependencies file (`requirements.txt`), we have to rebuild the image. And restart the `webserver` and `scheduler`.

### Image Customising

Basically we have to build it from airflow source code. Let's open a second terminal.

```bash
# cd to the directory desktop
cd ..

# clone the airflow source code
git clone https://github.com/apache/airflow.git
```

Open the source code in a new vscode window. First find the `docker-context-files` folder since every python dependency defined here will be installed automatically when building the image. Let's create a requirements text file in it. Build the image.

![30](./images/30.png)

```bash
docker build . --build-arg AIRFLOW_VERSION=
'2.7.3' --tag customising_airflow:latest
```

Next we need to replace the airflow name in the `yaml` file. Save the `yaml` file and recreate the docker containers for airflow webserver and scheduler:

```bash
docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler
```

Now you may wonder which methods to choose:

- In 99% of the cases, use the first method, which is extending the image since it's easy to use and build super fast.
- If you want more things to be customized, and really care about optimizing the image size. You need to customize the image.

## Airflow AWS S3 Sensor

Sensor is a special type of operator which waits for something to occur. It's a perfect tool for use cases in which you don't know exactly when the data will be available.

For example, your client will upload a csv file to the AWS S3 bucket daily but can be any time at the day. You basically need to check whether it's uploaded at a certain time interval before starting other tasks like downloading or cleaning.

MinIO is an object storage solution that provides an Amazon Web Services S3-compatible API and supports all core S3 features. MinIO is built to deploy anywhere - public or private cloud, baremetal infrastructure, orchestrated environments, and edge infrastructure. If you know how to build ETL with MinIO, you can easily apply it into AWS S3. Moreover, we can easily set up a MinIO service in a docker container (click [here](https://min.io/docs/minio/container/index.html) for more guidance).

```bash
docker run \
   -p 9000:9000 \
   -p 9001:9001 \
   --name minio \
   -v ~/minio/data:/data \
   -e "MINIO_ROOT_USER=ROOTNAME" \
   -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
   quay.io/minio/minio server /data --console-address ":9001"
```

We can see two ports are exposed:

```
API: http://172.17.0.2:9000  http://127.0.0.1:9000 
WebUI: http://172.17.0.2:9001 http://127.0.0.1:9001
```

Copy the WebUI URL and open it in the browser.

![31](./images/31.png)

Log in with the username and password above. Once logged in, we can create a bucket. Make sure we have the read and write permission.

![32](./images/32.png)

![33](./images/33.png)

Let's go back to vscode to generate a csv file which will be uploaded later to our airflow bucket. Create a folder named `data` in our root project directory. Then create a csv file called `data.csv`.

```
product_id, delivery_dt
1005, 2022-01-01
1006, 2021-02-01
```

Save it, and back to the browser to upload this file to our bucket.

![34](./images/34.png)

Let's start building an airflow dag to connect to our S3 bucket and sense the file's existence. Create a dag file named `dag_with_minio_s3.py` and open it.

To connect to the MinIO bucket we can use the AWS S3 API, which is included in the amazon airflow providers packages. Now change the image in the `yaml` file back to `apache/airflow:2.7.3`. Recreate the webserver and scheduler. Check the version of amazon providers:

```bash
docker ps

# enter the docker container
docker exec -it <scheduler container id> bash

# check the version of amazon provider
pip list | grep amazon
```

The output shows we have:

```
apache-airflow-providers-amazon          8.10.0
```

Go to the `8.10.0` docs: https://airflow.apache.org/docs/apache-airflow-providers-amazon/8.10.0/index.html (change on the left side to match our installed version)

Check the python api and look for [`airflow.providers.amazon.aws.sensors.s3`](https://airflow.apache.org/docs/apache-airflow-providers-amazon/8.10.0/_api/airflow/providers/amazon/aws/sensors/s3/index.html#module-airflow.providers.amazon.aws.sensors.s3). It says:

```
Waits for one or multiple keys (a file-like instance on S3) to be present in a S3 bucket.
The path is just a key/value pointer to a resource for the given S3 path. Note: S3 does not support folders directly, and only provides key/value pairs.
```

Go to the MinIO and click `Access Keys` and create a new one. Then add a new connection in Airflow.

```
{
  "aws_access_key_id": "mMitmTEMk------",
  "aws_secret_access_key": "ByUiI8pvus-------",
  "endpoint_url": "http://host.docker.internal:9000"
}
```

> Tips: here we use 'host.docker.internal' since we are running the services using docker.

![38](./images/38.png)

Create the following dag file.

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_minio',
    default_args=default_args,
    start_date=datetime(2024, 7, 22),
    schedule_interval='@daily'
) as dag:
    task1 = S3KeySensor(
        task_id='sensor_minio_s3',
        bucket_name='airflow',
        bucket_key='data.csv',
        aws_conn_id='minio_s3_conn'
    )
    
    task1
```

Run the dag and you might got error like:

```
botocore.exceptions.ClientError: An error occurred (403) when calling the HeadObject operation: Forbidden
```

To solve this, first check the network of the MinIO and Airflow containers.

```bash
docker inspect --format '{{.NetworkSettings.Networks}}' <container-id>
```

I checked and got this output:

```bash
(base) lbw1125@lbw1125deMacBook-Pro ~ % docker inspect --format '{{.NetworkSettings.Networks}}' <MinIO-container-id>
map[bridge:0xc0000d4600]
(base) lbw1125@lbw1125deMacBook-Pro ~ % docker inspect --format '{{.NetworkSettings.Networks}}' <airflow-container-id>
map[airflow-tutorial_default:0xc0004a8000]
```

We can see that MinIO is running on the bridge network while airflow is running on its user defined network. So the 2 services cannot communicate since they are not in the same network. Let's connect MinIO to the `airflow-tutorial_default` network.

```bash
(base) lbw1125@lbw1125deMacBook-Pro ~ % docker network connect airflow-tutorial_default <MinIO-container-id>
(base) lbw1125@lbw1125deMacBook-Pro ~ % docker inspect --format '{{.NetworkSettings.Networks}}' <MinIO-container-id>
map[airflow-tutorial_default:0xc000448000 bridge:0xc0004480c0]
```

Now the 2 services are in the same network. The dag can be run successfully.

![39](./images/39.png)

`Poke` is the default mode for sensor operators. Basically, it checks the file's existence at every poke_interval as long as it's within the timeout limit. Since the `data.csv` already exists in the airflow bucket, it finishes immediately after the first poking and is marked as success.

Let's go back to vscode, change the poke interval to 5 seconds and timeout to 30 seconds.

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_minio_v02',
    default_args=default_args,
    start_date=datetime(2024, 7, 22),
    schedule_interval='@daily'
) as dag:
    task1 = S3KeySensor(
        task_id='sensor_minio_s3',
        bucket_name='airflow',
        bucket_key='data.csv',
        aws_conn_id='minio_s3_conn',
        mode='poke',
        poke_interval=5,
        timeout=30
    )
    
    task1
```

Then we delete the `data.csv` from our airflow bucket. Let's pick the newest dag and start the sensor task again.

![40](./images/40.png)

We can see that it tried every 5 seconds until timeout. And it failed because the file doesn't exist. What if the `data.csv` is uploaded during the poking?

Let's rerun the dag and upload the `data.csv` in the meantime.

![45](./images/45.png)

We can see that it poked the file's existence right after we uploaded it!

## Airflow Hooks S3 PostgreSQL

Imagine we have a csv file called `Orders.csv` which contains artificial sales orders from March to June. It has 4 columns:

```
order_id,date,product_name,quantity
```

We need to first import it into our postgres database, then write a DAG to query data from it and upload it to the S3 bucket. Let's open DBeaver, connect to our postgres database. We're going to create a table called `orders` in the database `test`.

Right click the `test` and set as the default database. Then create a table called `orders` using the statement:

```postgresql
create table if not exists public.orders (
	order_id character varying,
  date date,
  product_name character varying,
  quantity integer,
  primary key (order_id)
)
```

Refresh the `test` database, we can see the `orders` table. Then we right click the table and import our `Orders.csv` file. We can see that the data has been imported successfully.

![46](./images/46.png)

Let's query the first 100 rows for double check.

```postgresql
select * from orders o limit 100
```

![47](./images/47.png)

Now let's create a dag to query data from it. Create a dag file called `dag_with_postgres_hook.py`. We are going to do 2 steps:

- query data from postgresql db and save into text file
- upload text file into s3

To query the data from postgres db, we need the **postgres hook**. Let's check the version of the installed postgres package. 

```bash
docker ps

# enter the docker container
docker exec -it <scheduler container id> bash

# check the version of amazon provider
pip list | grep postgres
```

```
apache-airflow-providers-postgres        5.7.1
```

Let's go to the airflow documentation, search and click the postgresql in the providers packages section. Select a version to match our local installation. Then click the python api. Go to the [hook](https://airflow.apache.org/docs/apache-airflow-providers-postgres/5.7.1/_api/airflow/providers/postgres/hooks/postgres/index.html) subpackages.

Hook is used to interact with Postgres DB and we can establish a connection to a postgres database via the `get_conn` function.

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook
```

We define a python function named `postgres_to_s3`:

```python
def postgres_to_s3():
    # step1: query data from postgresql db and save into text file
    
    # the conn_id can be found in the 'Connections' page in the Web UI
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    # connect to the db
    conn = hook.get_conn()
    # use cursor to execute our query
    cursor = conn.cursor()
    cursor.execute("select * from orders where date <= '20220501'")
    # return the data in a txt file
    with open("dags/get_orders.txt", "w") as f:
        csv_writer = csv.writer()
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerow(cursor)
    # close the cursor and conn
    cursor.close()
    conn.close()
    # logs
    logging.info("Saved orders data in text file get_orders.txt")
```

If we rerun the dag, we only get 1 txt file because the latter dag run will overwrite the txt file. Let's make sure we only get the orders data during the specific dag run's execution interval and save them with a dynamic text file name. In this way, they will not be overwritten. To achieve this, we have to give the current and next execution date to our python function. 

Let's open the airflow docs, select the installed airflow version which is `2.7.3`. Search for the macro, then click it. https://airflow.apache.org/docs/apache-airflow/2.7.3/templates-ref.html

There we find the `{{ ds_nodash }}` which is the execution date. Copy them and paste directly as the parameters of our python function since airflow will render those macros values during execution.

```jinja2
{{ next_ds_nodash }} the next execution date as YYYYMMDD if exists, else None
{{ ds_nodash }} Same as {{ dag_run.logical_date | ds_nodash }}.
```

```python
def postgres_to_s3(ds_nodash, next_ds_nodash):
    # step1: query data from postgresql db and save into text file
    
    # the conn_id can be found in the 'Connections' page in the Web UI
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from orders where date >= %s and date < %s", 
                   (ds_nodash, next_ds_nodash))
    # return the data in a txt file
    with open(f"dags/get_orders_{ds_nodash}.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerow(cursor)
    cursor.close()
    conn.close()
    logging.info("Saved orders data in text file: %s", f"dags/get_orders_{ds_nodash}.txt")
```

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import csv
import logging

default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def postgres_to_s3(ds_nodash, next_ds_nodash):
    # step1: query data from postgresql db and save into text file
    
    # the conn_id can be found in the 'Connections' page in the Web UI
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from orders where date >= %s and date < %s", 
                   (ds_nodash, next_ds_nodash))
    # return the data in a txt file
    with open(f"dags/get_orders_{ds_nodash}.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerow(cursor)
    cursor.close()
    conn.close()
    logging.info("Saved orders data in text file: %s", f"dags/get_orders_{ds_nodash}.txt")
    
    # step2: upload text file into s3
    
with DAG(
    dag_id='dag_with_postgres_hook_v02',
    default_args=default_args,
    start_date=datetime(2024, 7,22),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='postgres_to_s3',
        python_callable=postgres_to_s3
    )
    task1
```

Run the dag twice, we will find 2 txt files in vscode. Each with the execution date as the suffix.

<img src="./images/48.png" alt="48" style="zoom:50%;" />

These txt files only contain the order data which is between current and next execution date (since we are in 2024 now, and the data is old, so we didn't get any rows).

Now let's tackle step2, which is uploading the order text file into the S3 bucket. We need the S3 hook library to achieve this.

```bash
docker ps

# enter the docker container
docker exec -it <scheduler container id> bash

# check the version of amazon provider
pip list | grep amazon
```

```
apache-airflow-providers-amazon          8.10.0
```

Go to the airflow docs and select amazon of matching version. Click the python api and look for hood for s3.

```python
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
```

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

import csv
import logging

default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def postgres_to_s3(ds_nodash, next_ds_nodash):
    # step1: query data from postgresql db and save into text file
    
    # the conn_id can be found in the 'Connections' page in the Web UI
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from orders where date >= %s and date < %s", 
                   (ds_nodash, next_ds_nodash))
    # return the data in a txt file
    with open(f"dags/get_orders_{ds_nodash}.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerow(cursor)
    cursor.close()
    conn.close()
    logging.info("Saved orders data in text file: %s", f"dags/get_orders_{ds_nodash}.txt")
    
    # step2: upload text file into s3
    
    # the conn_id can be found in the Web UI
    s3_hook = S3Hook(aws_conn_id='minio_s3_conn')
    s3_hook.load_file(
        filename=f"dags/get_orders_{ds_nodash}.txt",
        key=f"orders/{ds_nodash}.txt",
        bucket_name="airflow",
        replace=True
    )
    
with DAG(
    dag_id='dag_with_postgres_hook_v03',
    default_args=default_args,
    start_date=datetime(2024, 7,22),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='postgres_to_s3',
        python_callable=postgres_to_s3
    )
    task1
```

Run the dag and go to the MinIO page. We can see in the `orders` folder, the txt file has been uploaded.

![49](./images/49.png)

If you don't want the txt files to exist in your vscode folder, python provides tempfile package which enables us to create files in the system temporary directory. 

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from tempfile import NamedTemporaryFile
import csv
import logging

default_args = {
    'owner': 'Bowen',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def postgres_to_s3(ds_nodash, next_ds_nodash):
    # step1: query data from postgresql db and save into text file
    
    # the conn_id can be found in the 'Connections' page in the Web UI
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from orders where date >= %s and date < %s", 
                   (ds_nodash, next_ds_nodash))
    # return the data in a txt file
    with NamedTemporaryFile(mode='w', suffix=f"{ds_nodash}") as f:
    #with open(f"dags/get_orders_{ds_nodash}.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerow(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info("Saved orders data in text file: %s", f"dags/get_orders_{ds_nodash}.txt")
        
        # step2: upload text file into s3
        
        # the conn_id can be found in the Web UI
        s3_hook = S3Hook(aws_conn_id='minio_s3_conn')
        s3_hook.load_file(
            # call the name attribute of the file object as filename
            filename=f.name,
            key=f"orders/{ds_nodash}.txt",
            bucket_name="airflow",
            replace=True
        )
        # replace the filename to the temporary file name which is f.name
        logging.info("Orders file %s has been pushed to S3!", f.name)
    
with DAG(
    dag_id='dag_with_postgres_hook_v04',
    default_args=default_args,
    start_date=datetime(2024, 7,22),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='postgres_to_s3',
        python_callable=postgres_to_s3
    )
    task1
```

Before uploading the file to S3, we need to flush the file object to that the text file is saved in disk. Our S3 `load_file` function should be inside of the `with` statement, bcz the temporary file will be deleted once exiting the context manager.

Delete the txt file in the bucket and run the new dag.

![50](./images/50.png)

From the log we can see the file has been uploaded successfully and there is no file existing in our vscode folder.

