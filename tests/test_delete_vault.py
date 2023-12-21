# tests/test_delete_vault.py
import unittest
from unittest.mock import patch, MagicMock
from app.delete_vault import delete_vault


class TestDeleteVault(unittest.TestCase):

    @patch('app.delete_vault.logging.getLogger')
    @patch('app.delete_vault.CredentialManager.get_glacier_client')
    def test_delete_vault(self, mock_get_glacier_client, mock_logger):
        mock_logger.return_value = MagicMock()

        # Mock Glacier client
        mock_glacier_client = MagicMock()
        mock_get_glacier_client.return_value = mock_glacier_client

        # Call the function
        delete_vault('test_vault')

        # Assert the delete_vault call
        mock_glacier_client.delete_vault.assert_called_with(
            accountId='-',
            vaultName='test_vault'
        )


if __name__ == '__main__':
    unittest.main()
