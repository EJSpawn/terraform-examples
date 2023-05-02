import boto3

def lambda_handler(event, context):
    bucket_name = 'some_bucket'

    client = boto3.client('athena')

    config = {
        'OutputLocation': 's3://' + bucket_name + '/',
        'EncryptionConfiguration': {'EncryptionOption': 'SSE_S3'}

    }

    # Query Execution Parameters
    sql = 'MSCK REPAIR TABLE some_database.some_table'
    context = {'Database': 'some_database'}

    client.start_query_execution(QueryString = sql, 
                                 QueryExecutionContext = context,
                                 ResultConfiguration = config)
