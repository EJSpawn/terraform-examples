import boto3
import pandas as pd

def lambda_handler(event, context):
    # Detalhes do arquivo do evento do S3
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Usando pandas para ler o Excel diretamente do S3
    file_path = f's3://{bucket_name}/{file_key}'
    df = pd.read_excel(file_path, engine='openpyxl')

    # Convertendo dataframe para CSV e enviando para outro diretório no mesmo bucket
    new_key = file_key.replace('source_directory', 'destination_directory').replace('.xlsx', '.csv')
    csv_buffer = df.to_csv(index=False)
    
    # Usando boto3 para salvar o CSV no S3
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, new_key).put(Body=csv_buffer)


import pytest
from moto import mock_s3
import boto3
from s3_transformer import lambda_handler

@pytest.fixture
def setup_s3():
    # Mocking S3
    mock = mock_s3()
    mock.start()
    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket='my_bucket')
    yield s3
    mock.stop()

def test_lambda_handler(setup_s3):
    s3 = setup_s3

    # Adicionando um arquivo Excel mock para o bucket S3
    with open('sample.xlsx', 'rb') as f:
        s3.Bucket('my_bucket').put_object(Key='source_directory/sample.xlsx', Body=f.read())

    # Simulando o evento do S3
    event = {
        'Records': [{
            's3': {
                'bucket': {
                    'name': 'my_bucket'
                },
                'object': {
                    'key': 'source_directory/sample.xlsx'
                }
            }
        }]
    }
    lambda_handler(event, None)

    # Verificar se o CSV foi criado e colocado no local correto
    objs = list(s3.Bucket('my_bucket').objects.filter(Prefix='destination_directory/sample.csv'))
    assert len(objs) == 1
    assert objs[0].key == 'destination_directory/sample.csv'



    pip install pytest moto pandas openpyxl boto3 s3fs