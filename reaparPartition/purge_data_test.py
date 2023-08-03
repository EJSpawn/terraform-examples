import unittest
from unittest.mock import patch, MagicMock
from your_module import purge_data  # Substitua 'your_module' pelo nome do seu módulo

class TestPurgeData(unittest.TestCase):
    @patch('boto3.client')
    @patch('boto3.resource')
    def test_purge_data(self, boto3_resource_mock, boto3_client_mock):
        # Criando o objeto de evento
        event = Event(
            task_type='purge_data',
            db_name='db_test',
            table_name='table_test',
            partition_columns=['column1_test', 'column2_test'],
            data_purge_params={}
        )

        # Configurando a resposta simulada para get_partition
        mock_partition = {
            'Partition': {
                'StorageDescriptor': {
                    'Location': 's3://mybucket/myprefix/'
                }
            }
        }
        glue_mock = MagicMock()
        glue_mock.get_partition.return_value = mock_partition
        boto3_client_mock.return_value = glue_mock

        # Configurando a resposta simulada para s3.Bucket e bucket.objects.filter
        mock_bucket = MagicMock()
        mock_objects = MagicMock()
        mock_bucket.objects.filter.return_value = mock_objects
        s3_resource_mock = MagicMock()
        s3_resource_mock.Bucket.return_value = mock_bucket
        boto3_resource_mock.return_value = s3_resource_mock

        # Chamando o método para teste
        purge_data(event)

        # Verificando se as chamadas aos métodos mockados foram feitas conforme o esperado
        boto3_client_mock.assert_called_with('glue')
        glue_mock.get_partition.assert_called_with(
            DatabaseName='db_test',
            TableName='table_test',
            PartitionValues=['column1_test', 'column2_test']
        )
        boto3_resource_mock.assert_called_with('s3')
        s3_resource_mock.Bucket.assert_called_with('mybucket')
        mock_bucket.objects.filter.assert_called_with(Prefix='myprefix')
        mock_objects.delete.assert_called_once()

if __name__ == '__main__':
    unittest.main()