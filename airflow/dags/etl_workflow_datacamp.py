from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

#Bash Operator example -------------------------------

default_args = {
  'owner': 'dsmith',
  'start_date': datetime(2023, 2, 12),
  'retries': 1
}

with DAG('etl_workflow_datacamp', default_args=default_args) as codependency_dag:

  task1 = BashOperator(task_id='first_task',
                     bash_command='echo 1',
                     dag=codependency_dag)

  task2 = BashOperator(task_id='second_task',
                     bash_command='echo 2',
                     dag=codependency_dag)

  task3 = BashOperator(task_id='third_task',
                     bash_command='echo 3',
                     dag=codependency_dag)

  # task1 must run before task2 which must run before task3
  task1 >> task2
  task2 >> task3
  #task3 >> task1

""" 
 #Python Operator example -------------------------------
 
def pull_file(URL, savepath):
  r = requests.get(URL)
  with open(savepath, 'wb') as f:
      f.write(r.content)   
  # Use the print method for logging
  print(f"File pulled from {URL} and saved to {savepath}")

from airflow.operators.python import PythonOperator

# Create the task
pull_file_task = PythonOperator(
    task_id='pull_file',
    # Add the callable
    python_callable=pull_file,
    # Define the arguments
    op_kwargs={'URL':'http://dataserver/sales.json', 'savepath':'latestsales.json'}
)

#Email Operator example -------------------------------

# Import the Operator
from airflow.operators.email import EmailOperator

# Define the task
email_manager_task = EmailOperator(
    task_id='email_manager',
    to='manager@datacamp.com',
    subject='Latest sales JSON',
    html_content='Attached is the latest sales JSON file as requested.',
    files='parsedfile.json',
    dag=process_sales_dag
)

# Set the order of tasks
pull_file_task >> email_manager_task


#scheduling -------------------------------

# Update the scheduling arguments as defined
default_args = {
  'owner': 'Engineering',
  'start_date': datetime(2023, 11, 1),
  'email': ['airflowresults@datacamp.com'],
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 3,
  'retry_delay': timedelta(minutes=20)
}

#Corre cada miércoles a las 12:30
dag = DAG('update_dataflows', default_args=default_args, schedule_interval='30 12 * * 3')


#sensor -------------------------------

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.sensors.filesystem import FileSensor

dag = DAG(
   dag_id = 'update_state',
   default_args={"start_date": "2023-10-01"}
)

precheck = FileSensor(
   task_id='check_for_datafile',
   filepath='salesdata_ready.csv',
   dag=dag)

part1 = BashOperator(
   task_id='generate_random_number',
   bash_command='echo $RANDOM',
   dag=dag
)

import sys
def python_version():
   return sys.version

part2 = PythonOperator(
   task_id='get_python_version',
   python_callable=python_version,
   dag=dag)
   
part3 = SimpleHttpOperator(
   task_id='query_server_for_external_ip',
   endpoint='https://api.ipify.org',
   method='GET',
   dag=dag)
   
precheck >> part3 >> part2
 """