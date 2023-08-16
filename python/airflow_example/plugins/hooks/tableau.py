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
        """
        Establishes and returns a connection to Tableau Server using username and password.
        Authentification with token is deprecated
        """
        tableau_auth = TSC.TableauAuth(self.conn.login, self.conn.password)
        server = TSC.Server(self.conn.host, use_server_version=True)
        server.auth.sign_in(tableau_auth)
        return server

    def refresh_extract(self, project_name, datasource_name):
        """
        Refreshes a specified extract on Tableau Server.
        """
        with self.get_conn() as server:
            # Get all projects on the server
            all_projects, _ = server.projects.get()
            # Find the project we're looking for
            project = next((project for project in all_projects if project.name == project_name), None)
            if not project:
                raise AirflowException(f"Project named '{project_name}' not found on Tableau Server.")
            
            # Get all datasources in the project
            all_datasources, _ = server.datasources.get(project_id=project.id)
            # Find the datasource we're looking to refresh
            datasource = next((ds for ds in all_datasources if ds.name == datasource_name), None)
            if not datasource:
                raise AirflowException(f"Datasource named '{datasource_name}' not found in project '{project_name}'.")
            
            # Refresh the datasource
            server.datasources.refresh(datasource)
