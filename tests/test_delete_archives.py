# tests/test_delete_archives.py
import unittest
from unittest.mock import patch, MagicMock
from app.delete_archives import delete_archive


class TestDeleteArchives(unittest.TestCase):

    @patch('app.delete_archives.logging.getLogger')
    @patch('app.delete_archives.CredentialManager.get_glacier_client')
    def test_delete_archive(self, mock_get_glacier_client, mock_logger):
        mock_logger.return_value = MagicMock()

        # Mock Glacier client
        mock_glacier_client = MagicMock()
        mock_get_glacier_client.return_value = mock_glacier_client

        # Call the function
        delete_archive('test_vault', 'test_archive_id')

        # Assert the delete_archive call
        mock_glacier_client.delete_archive.assert_called_with(
            accountId='-',
            vaultName='test_vault',
            archiveId='test_archive_id'
        )


if __name__ == '__main__':
    unittest.main()
