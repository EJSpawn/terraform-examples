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
        partition_directories = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('/')]

        # Extrair as datas (ano_mes_dia) das partições
        partitions = [os.path.dirname(directory).split('=')[1] for directory in partition_directories]

        # Obter partições existentes
        existing_partitions = glue.get_partitions(DatabaseName=database_name, TableName=table_name)
        existing_partition_values = [part['Values'][0] for part in existing_partitions['Partitions']]

        # Adicionar ou atualizar partições no Glue
        for ano_mes_dia in partitions:
            partition_location = f"s3://{bucket_name}/{partitions_directory}/ano_mes_dia={ano_mes_dia}"
            partition_input = {
                'Values': [ano_mes_dia],
                'StorageDescriptor': {
                    'Location': partition_location,
                    'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe',
                        'Parameters': {
                            'serialization.format': '1'
                        }
                    },
                    'Columns': [
                        # Defina as colunas do seu esquema aqui
                        {'Name': 'example_column', 'Type': 'string'}
                    ]
                }
            }

            # Verifica se a partição já existe
            if ano_mes_dia in existing_partition_values:
                # Se a partição existir, atualiza a partição
                glue.update_partition(DatabaseName=database_name, TableName=table_name, PartitionValueList=[ano_mes_dia], PartitionInput=partition_input)
            else:
                # Se a partição não existir, cria a partição
                glue.create_partition(DatabaseName=database_name, TableName=table_name, PartitionInput=partition_input)

        print(f"Partições adicionadas ou atualizadas: {partitions}")
    except ClientError as e:
        print(f"Erro ao adicionar ou atualizar partições: {e}")
