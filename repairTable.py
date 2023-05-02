import boto3

# Nome do banco de dados e da tabela no AWS Glue
database_name = 'my_database'
table_name = 'my_table'

# Caminho S3 onde os dados estão armazenados
s3_path = 's3://my-bucket/my-data/'

# Cria um cliente do AWS Glue e usa o mesmo role do Lambda
glue_client = boto3.client('glue')

def lambda_handler(event, context):

    # Chama o método repair_table para reparar as partições da tabela
    response = glue_client.repair_table(
        DatabaseName=database_name,
        TableName=table_name,
        PartitionPredicate={
            'Conditions': [
                {
                    'LogicalOperator': 'EQUALS',
                    'Key': 'location',
                    'Value': s3_path
                }
            ]
        }
    )

    # Retorna uma mensagem de sucesso
    return {'message': 'Table repaired successfully'}