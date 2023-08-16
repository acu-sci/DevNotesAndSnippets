from datetime import datetime
import airflow
from airflow import DAG
from operators.tableau import TableauRefreshOperator

default_args = {
    'start_date': airflow.utils.dates.days_ago(0)
}

dag = DAG(
    'refresh_tableau_extract',
    default_args=default_args,
    description='Refresh a Tableau Extract',
    schedule_interval=None,  # Manually triggered for this example
    catchup=False
)

refresh_tableau_task = TableauRefreshOperator(
    task_id='refresh_tableau_extract',
    tableau_conn_id='tableau_default',  # Assuming a connection setup in Airflow named 'tableau_default'
    project_name='my_project',
    datasource_name='my_datasource',
    dag=dag
)
