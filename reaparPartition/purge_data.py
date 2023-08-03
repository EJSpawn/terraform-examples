import boto3

def purge_data(event):
    # Criando os clientes do S3 e Glue
    s3 = boto3.resource('s3')
    glue = boto3.client('glue')

    # Obtendo os valores necessários do evento
    database_name = event.db_name
    table_name = event.table_name
    partition_values = event.partition_columns  # Assumindo que os valores da partição estão em partition_columns

    # Obtendo informações da partição
    response = glue.get_partition(
        DatabaseName=database_name,
        TableName=table_name,
        PartitionValues=partition_values
    )

    # Extraindo o caminho do bucket S3 dos dados da partição
    s3_path = response['Partition']['StorageDescriptor']['Location']
    bucket_name = s3_path.split('/')[2]  # Extraindo o nome do bucket do caminho S3
    prefix = '/'.join(s3_path.split('/')[3:])  # Extraindo o prefixo do caminho S3

    # Deletando os dados da partição no S3
    bucket = s3.Bucket(bucket_name)
    bucket.objects.filter(Prefix=prefix).delete()

    print(f"Purged data from {s3_path}")

    # Agora reutilizando o método delete_partitions para excluir a definição de partição no Glue Data Catalog
    delete_partitions(event)