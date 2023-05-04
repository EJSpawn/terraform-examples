import os
import boto3
from botocore.exceptions import ClientError

def reparar_particoes(event, context):
    # Configurar o cliente do Glue
    glue = boto3.client('glue')
    
    # Nome da tabela e caminho das partições
    table_name = event['table_name']
    partitions_directory = event['partitions_directory']
    database_name = event['database_name']
    s3 = boto3.client('s3')
    bucket_name = event['bucket_name']
    
    try:
        # Listar objetos no caminho das partições
        response = s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=partitions_directory
        )
        partition_directories = [obj['Key'] for obj in response['Contents']]

        # Extrair as datas (ano_mes_dia) das partições
        partitions = [os.path.basename(directory) for directory in partition_directories]

        # Adicionar partições no Glue
        for ano_mes_dia in partitions:
            partition_location = f"s3://{bucket_name}/{partitions_directory}/{ano_mes_dia}"
            glue.create_partition(
                DatabaseName=database_name,
                TableName=table_name,
                PartitionInput={
                    'Values': [ano_mes_dia],
                    'StorageDescriptor': {
                        'Location': partition_location,
                    }
                }
            )
        print(f"Partições adicionadas: {partitions}")
    except ClientError as e:
        print(f"Erro ao adicionar partições: {e}")