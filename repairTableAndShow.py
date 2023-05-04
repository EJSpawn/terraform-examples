import boto3
import os

glue_client = boto3.client('glue')
athena_client = boto3.client('athena')

glue_database = os.environ['GLUE_DATABASE']
glue_table = os.environ['GLUE_TABLE']

athena_query = "MSCK REPAIR TABLE " + glue_database + "." + glue_table
response = athena_client.start_query_execution(
    QueryString=athena_query,
    ResultConfiguration={
        'OutputLocation': 's3://<bucket-name>/athena/results/'
    }
)

query_execution_id = response['QueryExecutionId']
query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)['QueryExecution']['Status']['State']

if query_status == 'SUCCEEDED':
    partition_response = glue_client.get_partitions(
        DatabaseName=glue_database,
        TableName=glue_table
    )
    partitions = partition_response['Partitions']
    print("Partitions repaired: " + str(len(partitions)))
else:
    print("Query failed: " + query_status)