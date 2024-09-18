from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Definir una función que ejecutará la tarea
def mi_tarea():
    print("¡Hola, este es mi primer DAG!")

# Definir el DAG
with DAG(
    'my_first_dag',  # El ID del DAG
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2023, 9, 15),  # Fecha de inicio
        'retries': 1,  # Número de reintentos si falla
    },
    schedule_interval='@daily',  # Intervalo de ejecución, puede ser @daily, @hourly, etc.
    catchup=False,  # Si quieres que ejecute tareas en fechas pasadas
) as dag:

    # Crear una tarea usando PythonOperator
    tarea = PythonOperator(
        task_id='mi_tarea',
        python_callable=mi_tarea,  # La función que ejecutará
    )


