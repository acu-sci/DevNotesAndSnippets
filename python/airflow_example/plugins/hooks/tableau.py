# NOTE: Apparently there is already a provided tableau hook for airflow
# which is what you should use instead in a project.
# This hook works only as example on how to do a custom airflow hook and operator.

from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException
import tableauserverclient as TSC

class TableauHook(BaseHook):
    def __init__(self, tableau_conn_id='tableau_default'):
        self.tableau_conn_id = tableau_conn_id
        self.conn = self.get_connection(self.tableau_conn_id)
        
    def get_conn(self):
        tableau_auth = TSC.TableauAuth(self.conn.login, self.conn.password)
        server = TSC.Server(self.conn.host, use_server_version=True)
        server.auth.sign_in(tableau_auth)
        return server

    def refresh_extract(self, project_name, datasource_name):
        with self.get_conn() as server:
            all_projects, _ = server.projects.get()
            project = next((project for project in all_projects if project.name == project_name), None)
            if not project:
                raise AirflowException(f"Project named '{project_name}' not found on Tableau Server.")
            
            all_datasources, _ = server.datasources.get(project_id=project.id)
            datasource = next((ds for ds in all_datasources if ds.name == datasource_name), None)
            if not datasource:
                raise AirflowException(f"Datasource named '{datasource_name}' not found in project '{project_name}'.")
            
            # Start the refresh task
            refresh_task = server.datasources.refresh(datasource)
            return refresh_task.id  # Returning the task ID for reference

    def get_job_status(self, job_id):
        with self.get_conn() as server:
            status, _ = server.jobs.get_by_id(job_id)
            return status.status
        
    def get_latest_job_for_datasource(self, project_name, datasource_name):
        with self.get_conn() as server:
            all_jobs, _ = server.jobs.get()  # Get all jobs
            all_jobs = sorted(all_jobs, key=lambda j: j.created_at, reverse=True)  # Sort by created date
        
            # Filter jobs related to the datasource
            for job in all_jobs:
                # This assumes you have a way to determine if a job is related to your datasource.
                # This is a simple example that checks the job's notes attribute. Adjust based on your specifics.
                if datasource_name in job.notes:
                    return job.id
                
            return None

