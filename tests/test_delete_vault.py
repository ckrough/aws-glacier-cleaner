# tests/test_delete_vault.py
import unittest
from unittest.mock import patch, MagicMock
from app.delete_vault import delete_vault


class TestDeleteVault(unittest.TestCase):

    @patch('app.delete_vault.logging.getLogger')
    @patch('app.delete_vault.CredentialManager')
    @patch('app.delete_vault.boto3.client')
    def test_delete_vault(
        self, mock_boto_client, mock_credential_manager, mock_logger
    ):
        # Mock logging
        mock_logger.return_value = MagicMock()

        # Set up mock credentials
        mock_credentials = {
            'AccessKeyId': 'mock_key_id',
            'SecretAccessKey': 'mock_access_key',
            'SessionToken': 'mock_token'
        }
        mock_credential_manager.return_value.get_credentials.return_value = \
            mock_credentials

        # Mock Glacier client behavior
        mock_glacier_client = MagicMock()
        mock_boto_client.return_value = mock_glacier_client

        delete_vault('test_vault')
        mock_glacier_client.delete_vault.assert_called_with(
            accountId='-', vaultName='test_vault')


if __name__ == '__main__':
    unittest.main()
