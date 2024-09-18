from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.email import EmailOperator

# Update the scheduling arguments as defined
default_args = {
  'owner': 'JCGargola',
  'start_date': datetime(2024, 9, 17),
  'email': ['julianceci@gmail.com'],
  'email_on_failure': False,
  'email_on_retry': False,
  'email_on_success': True,
  'retries': 1000,
  'retry_delay': timedelta(minutes=5,seconds=30),
  'sla': timedelta(minutes=10)
}

dag = DAG(
   dag_id='dag_sensor', 
   default_args=default_args, 
   schedule_interval='59 * * * *'
)

precheck = FileSensor(
   task_id='check_for_datafile',
   filepath='/opt/airflow/dags/salesdata_ready.csv',
   dag=dag)

part1 = BashOperator(
   task_id='copy_file',
   bash_command='cp /opt/airflow/dags/salesdata_ready.csv /opt/airflow/dags/salesdata_ready_2.csv',
   dag=dag
)

precheck >> part1

#-------------------------------------------------------------------------------------------------------------------------------------

# import sys
# def python_version():
#    return sys.version

# part2 = PythonOperator(
#    task_id='get_python_version',
#    python_callable=python_version,
#    dag=dag)
   
# part3 = SimpleHttpOperator(
#    task_id='query_server_for_external_ip',
#    endpoint='https://api.ipify.org',
#    method='GET',
#    dag=dag)
   
# email_manager_task = EmailOperator(
#     task_id='email_manager',
#     to='manager@datacamp.com',
#     subject='Latest sales JSON',
#     html_content='Attached is the latest sales JSON file as requested.',
#     files='parsedfile.json',
#     dag=process_sales_dag
# )

# #Python Operator example -------------------------------
# def pull_file(URL, savepath):
#   r = requests.get(URL)
#   with open(savepath, 'wb') as f:
#       f.write(r.content)   
#   # Use the print method for logging
#   print(f"File pulled from {URL} and saved to {savepath}")

# # Create the task
# pull_file_task = PythonOperator(
#     task_id='pull_file',
#     # Add the callable
#     python_callable=pull_file,
#     # Define the arguments
#     op_kwargs={'URL':'http://dataserver/sales.json', 'savepath':'latestsales.json'}
# )
