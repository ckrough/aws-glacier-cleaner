# tests/test_glacier_vaults_list.py
import unittest
from unittest.mock import patch
from app.glacier_vaults_list import list_glacier_vaults
from botocore.exceptions import NoCredentialsError


class TestGlacierVaultsList(unittest.TestCase):

    @patch('app.glacier_vaults_list.boto3.client')
    def test_list_vaults(self, mock_client):
        mock_client.return_value.list_vaults.return_value = {
            'VaultList': [{'VaultName': 'TestVault1'}, {'VaultName': 'TestVault2'}]
        }

        result = list_glacier_vaults()
        self.assertEqual(result, ['TestVault1', 'TestVault2'])

    @patch('app.glacier_vaults_list.boto3.client')
    def test_no_credentials(self, mock_client):
        mock_client.side_effect = NoCredentialsError

        result = list_glacier_vaults()
        self.assertEqual(result, "No AWS credentials found")


if __name__ == '__main__':
    unittest.main()
