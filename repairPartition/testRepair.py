import boto3
import pytest
from moto import mock_s3, mock_glue
from your_lambda_file import reparar_particoes

@pytest.fixture
def setup_glue_and_s3():
    with mock_glue():
        glue = boto3.client("glue")
        glue.create_database(Name="test_db")
        glue.create_table(
            DatabaseName="test_db",
            TableInput={
                "Name": "test_table",
                "StorageDescriptor": {
                    "Columns": [{"Name": "example_column", "Type": "string"}],
                },
            },
        )

        with mock_s3():
            s3 = boto3.client("s3")
            s3.create_bucket(Bucket="test-bucket")
            yield glue, s3

def test_reparar_particoes(setup_glue_and_s3):
    glue, s3 = setup_glue_and_s3

    # Criar partições S3
    s3.put_object(Bucket="test-bucket", Key="test_part/ano_mes_dia=20220101/")
    s3.put_object(Bucket="test-bucket", Key="test_part/ano_mes_dia=20220102/")

    event = {
        "table_name": "test_table",
        "partitions_directory": "test_part",
        "database_name": "test_db",
        "bucket_name": "test-bucket",
    }
    reparar_particoes(event, None)

    # Verificar se as partições foram adicionadas
    partitions = glue.get_partitions(DatabaseName="test_db", TableName="test_table")["Partitions"]
    assert len(partitions) == 2
    assert {"Values": ["20220101"]} in partitions
    assert {"Values": ["20220102"]} in partitions

    # Atualizar partições S3
    s3.put_object(Bucket="test-bucket", Key="test_part/ano_mes_dia=20220102/")
    s3.put_object(Bucket="test-bucket", Key="test_part/ano_mes_dia=20220103/")

    reparar_particoes(event, None)

    # Verificar se as partições foram atualizadas e a nova partição foi adicionada
    partitions = glue.get_partitions(DatabaseName="test_db", TableName="test_table")["Partitions"]
    assert len(partitions) == 3
    assert {"Values": ["20220101"]} in partitions
    assert {"Values": ["20220102"]} in partitions
    assert {"Values": ["20220103"]} in partitions