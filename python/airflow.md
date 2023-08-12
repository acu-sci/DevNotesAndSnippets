# Create an Airflow DAG
The DAG is defined through a python script which can be uploaded to the Airflow UI.  
``` python
import airflow
import os

# airflow modules
from airflow import DAG
# get DataFlow operator
from airflow.contrib.operators.dataflow_operator import DataflowTemplateOperator
from airflow.models import Variable
# get Bucket operator
from airflow.operator.gce_container_plugin import GceInstanceStartContainerOperator
from airflow.utils.dates import days_ago
# useful to measure performance
from datetime import timedelta

# Define DAG parameters in a dictionary
# This dictionary can be passed to a DAG object
default_args = {
    'start_date' = days_ago(0), #today
    'dataflow_default_options' : {
        'project': Variable.get("project_id"),
        'region': Variable.get("region"),
        'tempLocation':f'gs://{Variable.get("df_bucket_loc_template_loc")}',
        ...
    }
}

# Create a DAG object
dag = DAG(
    'dag_name',
    default_args = default_args,
    description = 'lalalala',
    schedule_interval = None, # This can be set to run the DAG periodically
    dagrun_timeout=timedelta(minutes=20) # expected maximum job run time
)

# Call DataFlow Job from DAG using the DataFlowTemplateOperator
# A DAG is per se a collection of tasks
dag_tasks = {}
dag_taks[0] = DataflowTemplateOperator(
    task_id= ,
    template= ,
    parameters={
        #template parameters
    },
    gcp_conn_id= , # defie your connection that has access to other services in GCP (Bucket/secrets?)
    dag=dag
)

# further define what the dag should do

```
You can use the operators to run stuff with DAGs. For example the PythonOperator allows you to run python scripts  

---  
  
# Create a Plugin
## Hook
Create a personalized hook creating a class out of the Airflow BaseHook class (inheritance)
``` python
from airflow.hooks.base_hook import BaseHook


class MyNewHook(BaseHook):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

```
## Operator
Create a personalized operator creating a class out of the Airflow BaseOperator
``` python
from airflow.operators import BaseOperator


class MyNewOperator(BaseOperator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hook = None

    def excecute(self, context):
        """
        This method is called when the dag with the operator call is excecuted
        """
        if not self.hook:
            self.hook = MyNewHook(...)
        # call hook methods
        self.hook.method1()


```

## Use the Operator in a DAG
``` python
import airflow
from airflow import DAG

from operators_folder.my_operator import MyNewOperator

default_args = {
    'start_date': airflow.utils.dates.days_ago(0)}

dag = DAG(
    'dag_test', # DAG name
    default_args=default_args,
    description='What does this DAG do',
    schedule_interval=None, # no inherent periodicity
    dagrun_timeout=timedelta(minutes=20)) # max run time

operator_dag = {}

operator_dag[sort_id] = MyNewOperator(
      **arguments_dict,
      dag=dag)


```


# Exceptions
raise an exception with the defined Airflow package
``` python
from airflow.exceptions import AirflowException

result = app.method1()

if 'result_key' in result:
    output = result['result_key']
else:
    raise AirflowException(f'No result optained from API call:'
                            f' {result.get("error_description")}')

```