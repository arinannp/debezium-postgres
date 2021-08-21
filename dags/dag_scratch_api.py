from datetime import timedelta
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.dummy_operator import DummyOperator
from scrape_api import reset_scraping_status, update_scraping_status, update_covid_data


URL = "https://data.covid19.go.id/public/api/update.json"
DB_NAME = "covid"
DB_USER = "debezium"
DB_PASSWORD = "debezium"
DB_HOST = "postgres-db"
DB_PORT = "5432"
CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
TABLE_NAME_COVID = "covid_api"
TABLE_NAME_SCRAPE = "last_scratch"

args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'email': ['test@mail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    dag_id="debezium-implementation",
    default_args=args,
    description="debezium implementation to cdc your data",
    schedule_interval="55 15 * * *",
    start_date=days_ago(2),
    tags=['debezium-project']
)

start = DummyOperator(
    task_id='start',
    dag=dag
)

task_1 = PythonOperator(
    task_id='reset_last_scraping_status',
    python_callable=reset_scraping_status.reset_last_scratch,
    op_kwargs={'db_name': DB_NAME, 'table_name': TABLE_NAME_SCRAPE, 'connection_string': CONNECTION_STRING},
    dag=dag
)

task_2 = PythonOperator(
    task_id='update_status_last_scraping',
    python_callable=update_scraping_status.get_new_update,
    op_kwargs={'db_name': DB_NAME, 'table_name': TABLE_NAME_SCRAPE, 'connection_string': CONNECTION_STRING},
    dag=dag
)

task_3 = PythonOperator(
    task_id='update_covid_data',
    python_callable=update_covid_data.update_new_data,
    op_kwargs={'api_url': URL,'db_name': DB_NAME, 'table_name': TABLE_NAME_COVID, 'connection_string': CONNECTION_STRING},
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

start >> task_1 >> task_2 >> task_3 >> end