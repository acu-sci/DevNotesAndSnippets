# Google Cloud

## Google SDK

After installing the Google SDK, you can start using it by running:

```
gcloud init
```

List all configurations:

```
gcloud config configurations list
```

Create a new configuration:

```
gcloud config configurations create <name>
```

List attributes of active config:

```
gcloud config list
```

Set configuration parameters:

```
gcloud config set account <account-email> 
gcloud config set project <project-id>   
gcloud config set compute/region <region>  
gcloud config set compute/zone <zone> 
```

You can use your credentials to authenticate. First, go to the Google Cloud Console. Select your project and go to APIs & Services > Credentials. Create a new service account, download the JSON key file, and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the JSON key file`

Use credentials to login:

```
gcloud auth application-default login
```

List accounts with login info:

```
gcloud auth list
```

## Airflow DAGs

**Directed Acyclic Graphs (DAGs):** DAGs are a central concept in Airflow. A DAG is a collection of tasks that run with a specific order determined by their dependencies. DAGs are ideal for Extract, Transform, Load tasks, providing a structure for efficient data pipeline management.

**Operator Instances:** In Airflow, each task is an instance of an operator class. Tasks are parameterized with a set of input arguments, providing flexibility and customization for complex workflows. An example of an operator is the DataflowTemplateOperator() which is used for Google Dataflow tasks.  

## Google Cloud Composer and Airflow DAGs

**Managed Environment:** Google Cloud Composer is a managed Apache Airflow service. Helps create, schedule, monitor, and manage workflows.

**Instance Startup:** When a Composer environment is created, instances are also created. You can configure the number of nodes in the environment at the time of environment creation.

**Worker Instances:** The actual tasks of a DAG are executed in separate worker instances. These instances are managed automatically by Cloud Composer, providing flexibility and reliability for task execution.

**Orchestrator Instance:** The scheduling and orchestration of DAGs are managed by separate web server and scheduler instances. This division of responsibilities ensures that your DAGs are monitored and executed accurately.

**Multiple DAGs:** One of the powerful features of Composer and Airflow is that multiple DAGs can run simultaneously, each in its own worker instance. These worker instances are automatically scaled according to the needs of the running DAGs, ensuring resource efficiency.


## BigQuery

Data in BigQuery is organized within projects. Within a project, you have datasets, and within these datasets, you have tables that contain the actual data.

It is particularly powerful for querying nested data structures, such as those found in JSON files.

Assuming there's a table in BigQuery linked to your JSON data source, you can query it directly. For example, if you have a `users` table with nested `addresses`:

```sql
SELECT
  user_id,
  name,
  email,
  addresses.type AS address_type,
  addresses.street AS street,
  addresses.city AS city,
  addresses.state AS state,
  addresses.zip AS zip
FROM
  `project-id.dataset-id.users`,
  UNNEST(addresses) AS addresses
```

The query will retrieve user information and address details by flattening the nested `addresses` array. In the result, you will get each address as a separate row along with the corresponding user details.

In addition to querying data, you can also query metadata of a dataset or a table in BigQuery. For instance, the following query retrieves all schemas in the current dataset excluding the schema owner:

```sql
SELECT
  * EXCEPT(schema_owner)
FROM
  `project-id.dataset-id`.INFORMATION_SCHEMA.SCHEMATA
```


If you're interested in metadata of a specific table, you can query the `INFORMATION_SCHEMA.COLUMNS` view for that table:

```sql
SELECT 
  column_name, 
  data_type,
  is_nullable
FROM 
  `project-id.dataset-id.INFORMATION_SCHEMA.COLUMNS`
WHERE 
  table_name = 'your_table_name'
```
