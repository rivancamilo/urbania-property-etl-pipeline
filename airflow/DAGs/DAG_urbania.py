# dags/xml_to_mysql_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import logging


default_args = {
    'owner': 'Ivan Camilo Rosales',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Definición del DAG
with DAG(
    'xml_to_mysql_etl',
    default_args=default_args,
    description='ETL para procesar XML y cargar a MySQL usando contenedor Python',
    schedule_interval='@daily',
    catchup=False,
    tags=['etl', 'xml', 'mysql', 'docker'],
) as dag:
    
    run_etl = DockerOperator(
        task_id='run_python_etl',
        image='python-etl:latest',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='project_etl_network',
        environment={
            'DB_HOST': 'mysql',
            'DB_USER': 'etl_user',
            'DB_PASSWORD': 'etl_password',
            'DB_NAME': 'bdUrbania',
            'DB_PORT': '3306',
            'XML_FILE': '/app/data/data.xml',
            'TABLE_NAME': 'usuarios'
        },
        mounts=[
            {
                'source': '/home/claude/data',
                'target': '/app/data',
                'type': 'bind'
            }
        ],
    )
    
    
    #Definir orden de ejecución
    run_etl


