# tests/test_glacier_vaults_list.py
import unittest
from unittest.mock import patch, MagicMock
from app.glacier_vaults_list import list_glacier_vaults


class TestGlacierVaultsList(unittest.TestCase):

    @patch('app.glacier_vaults_list.logging.getLogger')
    @patch('app.glacier_vaults_list.boto3.client')
    def test_list_glacier_vaults(self, mock_boto_client, mock_logger):
        # Mock logging
        mock_logger.return_value = MagicMock()

        # Mock Boto3 client response
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_client.list_vaults.return_value = {
            'VaultList': [
                {'VaultName': 'TestVault1'},
                {'VaultName': 'TestVault2'}
            ]
        }

        result = list_glacier_vaults()
        self.assertEqual(result, ['TestVault1', 'TestVault2'])


if __name__ == '__main__':
    unittest.main()
