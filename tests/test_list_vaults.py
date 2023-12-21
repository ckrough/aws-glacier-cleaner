# tests/test_list_vaults.py
import unittest
from unittest.mock import patch, MagicMock
from app.list_vaults import list_vaults
from botocore.exceptions import NoCredentialsError, ClientError


class TestListVaults(unittest.TestCase):
    """
    Unit tests for the list_vaults function in app/list_vaults.py.
    """

    @patch('app.list_vaults.CredentialManager.get_glacier_client')
    @patch('app.list_vaults.logging.getLogger')
    def test_list_vaults_success(self, mock_logger, mock_get_glacier_client):
        """
        Test successful retrieval of vault names from AWS Glacier.
        """
        mock_logger.return_value = MagicMock()

        # Mock Glacier client and successful response
        mock_glacier_client = MagicMock()
        mock_get_glacier_client.return_value = mock_glacier_client
        mock_glacier_client.list_vaults.return_value = {
            'VaultList': [{'VaultName': 'Vault1'}, {'VaultName': 'Vault2'}]
        }

        result = list_vaults()
        self.assertEqual(result, ['Vault1', 'Vault2'])

    @patch('app.list_vaults.CredentialManager.get_glacier_client')
    @patch('app.list_vaults.logging.getLogger')
    def test_list_vaults_no_credentials_error(self, mock_logger,
                                              mock_get_glacier_client):
        """
        Test handling of NoCredentialsError when listing vaults.
        """
        mock_logger.return_value = MagicMock()

        # Mock Glacier client and NoCredentialsError
        mock_glacier_client = MagicMock()
        mock_get_glacier_client.return_value = mock_glacier_client
        mock_glacier_client.list_vaults.side_effect = NoCredentialsError()

        result = list_vaults()
        self.assertEqual(result, "No AWS credentials found")

        # Ensure that the logger's error method was called
        mock_logger.return_value.error.assert_called_once_with(
            "No AWS credentials found")


if __name__ == '__main__':
    unittest.main()
