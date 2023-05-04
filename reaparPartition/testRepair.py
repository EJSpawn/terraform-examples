import boto3
import json
import os
import pytest
from moto import mock_glue, mock_s3
from reparar_particoes import reparar_particoes

@pytest.fixture
def setup_s3_partitions():
    s3 = boto3.client("s3")
    bucket_name = "test-bucket"
    s3.create_bucket(Bucket=bucket_name)
    partitions_directory = "partitions"
    partitions = ["20220101", "20220102", "20220103"]
    for partition in partitions:
        s3.put_object(Bucket=bucket_name, Key=f"{partitions_directory}/{partition}/data.parquet", Body=b"test data")
    return bucket_name, partitions_directory, partitions

@pytest.fixture
def setup_glue_table():
    glue = boto3.client("glue")
    database_name = "test_db"
    table_name = "test_table"
    glue.create_database(DatabaseInput={"Name": database_name})
    glue.create_table(
        DatabaseName=database_name,
        TableInput={
            "Name": table_name,
            "PartitionKeys": [{"Name": "ano_mes_dia", "Type": "string"}],
            "StorageDescriptor": {
                "Columns": [{"Name": "example_column", "Type": "string"}],
                "Location": "",
            },
        },
    )
    return database_name, table_name

@mock_s3
@mock_glue
def test_reparar_particoes(setup_s3_partitions, setup_glue_table):
    bucket_name, partitions_directory, partitions = setup_s3_partitions
    database_name, table_name = setup_glue_table
    glue = boto3.client("glue")

    # Atualizar a localização da tabela com o bucket e diretório correto
    glue.update_table(
        DatabaseName=database_name,
        TableInput={
            "Name": table_name,
            "StorageDescriptor": {
                "Location": f"s3://{bucket_name}/{partitions_directory}/",
            },
        },
    )

    # Invocar a função Lambda
    event = {
        "table_name": table_name,
        "partitions_directory": partitions_directory,
        "database_name": database_name,
        "bucket_name": bucket_name,
    }
    reparar_particoes(event, None)

    # Verificar se as partições foram adicionadas corretamente
    for partition in partitions:
        response = glue.get_partition(DatabaseName=database_name, TableName=table_name, PartitionValues=[partition])
        assert response["Partition"]["Values"][0] == partition