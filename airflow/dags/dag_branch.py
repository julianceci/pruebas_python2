from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.bash import BashOperator

# Create a function to determine if years are different
def year_check(**kwargs):
    current_year = int(kwargs['ds_nodash'][0:4])
    previous_year = int(kwargs['prev_ds_nodash'][0:4])
    if current_year == previous_year:
        return 'current_year_task'
    else:
        return 'new_year_task'

with DAG(dag_id='branch_dag', default_args={'owner': 'airflow'}, start_date=datetime(2024, 9, 17)) as dag:
  current_year_task = BashOperator(task_id='current_year_task', bash_command='echo current_year_task')
  new_year_task = BashOperator(task_id='new_year_task', bash_command='echo new_year_task')
  # Define the BranchPythonOperator
  branch_task = BranchPythonOperator(task_id='branch_task', python_callable=year_check, provide_context=True)

# Define the dependencies
branch_task >> current_year_task
branch_task >> new_year_task