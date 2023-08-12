"""
This script provides a command-line interface for running Google Cloud Dataflow jobs. 

It takes several arguments:
- Google Cloud Project ID
- Unique Dataflow Job name
- Google Cloud Storage Path to the Dataflow Template
- Path to the service account credentials file

In addition to the above, it also takes a list of template parameters as additional command-line arguments. 

The `run` function is the core of this script. It builds a request to launch the Dataflow template with the provided parameters 
and executes the request. The response from the Dataflow service is then returned.

In the main part parses the command-line arguments and template parameters. These are used to create a `run` 
function call. The response from this call (i.e., the response from the Dataflow service) is printed to the console.

Command-line arguments and parameters take priority over configuration files. This means that any arguments or parameters 
passed on the command line will overwrite those specified in the configuration file.

In essence, this script enables the user to start a Google Cloud Dataflow job from the command line, or job orchestration service, which can be very useful 
for automating and scheduling Dataflow jobs.

Example of calling this job:

python run_dataflow_template.py \
--project myproject-dev \
--job run_etl_bigquery_1 \
--credentials-file="/mnt/c/Users/me/path-to-project/.cred/creds-dev-1234.json" \
--template gs://bucketpath/templates/dataflow-bq \
--bqSourceProjectId "$BQ_SOURCE_PROJECT_ID" \
--bqSourceDatasetName "$BQ_SOURCE_DATASET_NAME" \
--bqSourceTableName "$BQ_SOURCE_TABLE_NAME" \
--gcsBucket "$GCS_BUCKET" \
--gcsTempPath "$GCS_TEMP_PATH" \
--gcsSqlFile "$GCS_SQL_FILE" \
"""

import json
import argparse
import configparser
from googleapiclient.discovery import build
from google.oauth2 import service_account

def run(project, job, template, credentials_file, parameters=None):
    """Runs a Dataflow template.

    Args:
        project (str): Google Cloud project ID.
        job (str): Unique Dataflow job name.
        template (str): GCS path to Dataflow template.
        credentials_file (str): Path to the service account credentials file.
        parameters (dict, optional): Parameters for the template. Defaults to None.

    Returns:
        dict: The response from the Dataflow service.
    """
    parameters = parameters or {}

    # Initialize service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file
    )

    # Build the dataflow service
    dataflow = build('dataflow', 'v1b3', credentials=credentials)

    # Define the request to launch the Dataflow template
    request = dataflow.projects().locations().templates().launch(
        projectId=project,
        gcsPath=template,
        location="europe-west1",
        body={
            'jobName': job,
            'parameters': parameters,
        }
    )

    # Execute the request
    response = request.execute()

    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Define command-line arguments
    parser.add_argument('--project', help='Google Cloud project ID.')
    parser.add_argument('--job', help='Unique Dataflow job name.')
    parser.add_argument('--template', help='GCS path to Dataflow template.')
    parser.add_argument('--credentials-file', help='Path to service account credentials file.')
    parser.add_argument('--config', help='Selected section in the config file.')
    parser.add_argument('--config-file', default="scheduling/parameter.ini", help='Path to the config file.')

    # Parse known command-line arguments and any remaining arguments
    args, unknown_args = parser.parse_known_args()

    # Define a new argument parser for template parameters
    template_argparser = argparse.ArgumentParser()

    # Add each unknown argument as a command-line argument
    for arg in unknown_args:
        if arg.startswith('-'):
            template_argparser.add_argument(arg)

    # Parse the template parameters from the command-line arguments
    parameters = template_argparser.parse_args(unknown_args)

    # Create a config parser to read the configuration file
    parser_config = configparser.ConfigParser()
    parser_config.optionxform=str
    parser_config.read(args.config_file)

    parsed_section = {}
    if args.config:
        for key in parser_config._sections[args.config]:
            parsed_section[key] = parser_config.get(args.config, key)

    # Merge the parsed arguments and the configuration file
    parsed_config = {**parsed_section, **args.__dict__, **parameters.__dict__}

    # Define the project, job, template, and credentials from the parsed configuration
    arg_project = parsed_config["project"]
    arg_job = parsed_config["job"]
    arg_template = parsed_config["template"]
    arg_credentials_file = parsed_config["credentials_file"]

    # Define the template parameters from the parsed configuration
    parameter_key_values = [
        "bqSourceProjectId",
        "bqSourceDatasetName",
        "bqSourceTableName",
        "gcsBucket",
        "gcsTempPath",
        "gcsSqlFile"
    ]

    matched_parameters = {key: parsed_config[key] for key in parameter_key_values if parsed_config.get(key)}

    # Run the Dataflow template and print the response
    response = run(
        project=arg_project,
        job=arg_job,
        template=arg_template,
        credentials_file=arg_credentials_file,
        parameters=matched_parameters,
    )
    print(json.dumps(response, indent=2))
