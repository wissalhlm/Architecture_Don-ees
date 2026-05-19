from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'job_pipeline_dag',
    default_args=default_args,
    description='Pipeline de données: Scraping -> Cleaning -> Analyse',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
    tags=['jobs', 'pipeline'],
) as dag:

    scrape_task = BashOperator(
        task_id='scrape_data',
        bash_command='cd /opt/airflow/project && python scraping.py',
    )

    clean_task = BashOperator(
        task_id='clean_data',
        bash_command='cd /opt/airflow/project && python cleaning.py',
    )

    analyse_task = BashOperator(
        task_id='analyse_data',
        bash_command='cd /opt/airflow/project && python analyse.py',
    )

    # Définition de l'ordre d'exécution
    scrape_task >> clean_task >> analyse_task
