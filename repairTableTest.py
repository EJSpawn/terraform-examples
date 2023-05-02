import boto3
from moto import mock_glue
import unittest
from lambda_function import lambda_handler

class TestGlueRepair(unittest.TestCase):

    def setUp(self):
        # Inicializa o mock do AWS Glue
        self.glue = mock_glue()
        self.glue.start()

        # Cria um cliente do AWS Glue
        self.client = boto3.client('glue')

    def tearDown(self):
        # Para o mock do AWS Glue
        self.glue.stop()

    def test_repair_table(self):
        # Define o nome do banco de dados e da tabela
        database_name = 'my_database'
        table_name = 'my_table'

        # Define o caminho S3 onde os dados estão armazenados
        s3_path = 's3://my-bucket/my-data/'

        # Cria um banco de dados no AWS Glue
        self.client.create_database(
            DatabaseInput={'Name': database_name})

        # Cria uma tabela no AWS Glue
        self.client.create_table(
            DatabaseName=database_name,
            TableInput={
                'Name': table_name,
                'StorageDescriptor': {
                    'Location': s3_path,
                    'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
                        'Parameters': {'field.delim': ','}
                    },
                    'Columns': [{'Name': 'id', 'Type': 'int'}]
                }
            }
        )

        # Chama a função lambda_handler para reparar as partições da tabela
        result = lambda_handler(None, None)

        # Verifica se a função retornou uma mensagem de sucesso
        self.assertEqual(result['message'], 'Table repaired successfully')

        # Obtém as informações da tabela reparada
        response = self.client.get_table(DatabaseName=database_name, Name=table_name)

        # Verifica se as partições foram reparadas corretamente
        partitions = response['Table']['PartitionKeys']
        self.assertEqual(len(partitions), 1)
        self.assertEqual(partitions[0]['Name'], 'ano_mes_dia')
        self.assertEqual(partitions[0]['Type'], 'string')
        
        self.tearDown()