def test_delete_glue_partition():
    # Configurando o mock
    glue_client = boto3.client('glue', region_name='us-east-1')
    
    database_name = 'test_database'
    table_name = 'test_table'
    partition_values = ['2023', '01', '01']

    # Criando um banco de dados e uma tabela mock para o teste
    glue_client.create_database(DatabaseInput={'Name': database_name})
    glue_client.create_table(
        DatabaseName=database_name,
        TableInput={
            'Name': table_name,
            'PartitionKeys': [{'Name': 'year', 'Type': 'string'}, {'Name': 'month', 'Type': 'string'}, {'Name': 'day', 'Type': 'string'}]
        }
    )
    glue_client.create_partition(
        DatabaseName=database_name,
        TableName=table_name,
        PartitionInput={'Values': partition_values}
    )
    
    # Executando a função
    response = delete_glue_partition(database_name, table_name, partition_values)

    # Verificando se a partição foi realmente deletada
    with pytest.raises(glue_client.exceptions.EntityNotFoundException):
        glue_client.get_partition(DatabaseName=database_name, TableName=table_name, PartitionValues=partition_values)