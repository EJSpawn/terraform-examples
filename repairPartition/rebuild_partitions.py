def rebuild_partitions(event):
    # Criando o cliente do Glue
    client = boto3.client('glue')

    # Obtendo os valores necessários do evento
    database_name = event.db_name
    table_name = event.table_name
    partition_values = event.partition_columns  # Assumindo que os valores da partição estão em partition_columns

    # Excluindo a partição
    delete_response = client.delete_partition(
        DatabaseName=database_name,
        TableName=table_name,
        PartitionValues=partition_values
    )

    print(f"Deleted partition in {database_name}.{table_name} with columns {partition_values}")

    # Recriando a partição (assumindo que o StorageDescriptor é o mesmo para a nova partição)
    create_response = client.create_partition(
        DatabaseName=database_name,
        TableName=table_name,
        PartitionInput={
            'Values': partition_values,
            'StorageDescriptor': delete_response['Partition']['StorageDescriptor']
        }
    )

    print(f"Created partition in {database_name}.{table_name} with columns {partition_values}")