import sys
from datetime import datetime
import boto3
from pyspark.sql import SparkSession

# Função principal
def main():
    # Recebendo parâmetros
    db_name = sys.argv[1]
    tb_name = sys.argv[2]
    partition_name = sys.argv[3]
    retention_days = int(sys.argv[4])

    # Criando a sessão Spark
    spark = SparkSession.builder \
        .appName('Glue Purge Job') \
        .getOrCreate()

    # Inicializando boto3 clients
    glue_client = boto3.client('glue')
    s3_client = boto3.client('s3')

    # Coletando as partições da tabela
    partitions = get_partitions(glue_client, db_name, tb_name)

    # Identificando as partições a serem deletadas
    partitions_to_delete = identify_partitions_to_delete(partitions, partition_name, retention_days)

    # Deletando as partições no Glue Catalog e no S3
    delete_partitions(glue_client, s3_client, db_name, tb_name, partitions_to_delete)

    # Parando a sessão Spark
    spark.stop()

def get_partitions(glue_client, db_name, tb_name):
    partitions = []
    paginator = glue_client.get_paginator('get_partitions')
    for page in paginator.paginate(DatabaseName=db_name, TableName=tb_name):
        partitions.extend(page['Partitions'])
    return partitions

def identify_partitions_to_delete(partitions, partition_name, retention_days):
    # Ordenando as partições pelo valor da partição
    sorted_partitions = sorted(partitions, key=lambda p: p['Values'][0], reverse=True)

    # Mantendo apenas as n partições mais recentes
    partitions_to_keep = sorted_partitions[:retention_days]

    # Identificando as partições a serem deletadas
    partitions_to_delete = [p for p in sorted_partitions if p not in partitions_to_keep]
    return partitions_to_delete

def delete_partitions(glue_client, s3_client, db_name, tb_name, partitions_to_delete):
    for partition in partitions_to_delete:
        partition_value = partition['Values'][0]
        location = partition['StorageDescriptor']['Location']

        # Deletando a partição no Glue Catalog
        glue_client.delete_partition(DatabaseName=db_name, TableName=tb_name, PartitionValues=[partition_value])

        # Deletando os dados no S3
        delete_s3_data(s3_client, location)

def delete_s3_data(s3_client, location):
    bucket = location.split('/')[2]
    prefix = '/'.join(location.split('/')[3:])

    # Listando os objetos no S3
    objects_to_delete = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if 'Contents' in objects_to_delete:
        for obj in objects_to_delete['Contents']:
            s3_client.delete_object(Bucket=bucket, Key=obj['Key'])

if __name__ == "__main__":
    main()
