from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException
from hooks.tableau import TableauHook
import time

class TableauRefreshOperator(BaseOperator):
    @apply_defaults
    def __init__(self,
                 tableau_conn_id='tableau_default',
                 project_name='',
                 datasource_name='',
                 polling_interval=60,
                 timeout=3600,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tableau_conn_id = tableau_conn_id
        self.project_name = project_name
        self.datasource_name = datasource_name
        self.polling_interval = polling_interval
        self.timeout = timeout
        self.hook = None

    def wait_on_completion(self, hook, job_id):
        start_time = time.time()
        while (time.time() - start_time) < self.timeout:
            job_status = hook.get_job_status(job_id)
            self.log.info(f"Job {job_id} status: {job_status}")
            
            if job_status == 'Finished':
                return
            elif job_status in ['Failed', 'Canceled']:
                raise AirflowException(f"Job {job_id} ended with status: {job_status}")
            
            time.sleep(self.polling_interval)

        raise AirflowException(f"Job {job_id} did not complete within {self.timeout} seconds.")

    def execute(self, context):
        if not self.hook:
            self.hook = TableauHook(tableau_conn_id=self.tableau_conn_id)
    
        # Check if there's an ongoing refresh job
        current_job_id = self.hook.get_latest_job_for_datasource(self.project_name, self.datasource_name)
        if current_job_id:
            current_job_status = self.hook.get_job_status(current_job_id)
            if current_job_status not in ['Finished', 'Failed', 'Canceled']:  # The job is still running
                self.log.info(f"Waiting for ongoing job {current_job_id} to complete...")
                self.wait_on_completion(self.hook, current_job_id)

        # Start a new refresh job
        new_job_id = self.hook.refresh_extract(self.project_name, self.datasource_name)
        self.log.info(f"Started new job with ID: {new_job_id}")
    
        # Wait for the new refresh job to complete
        self.wait_on_completion(self.hook, new_job_id)
