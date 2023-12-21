# tests/test_delete_archives.py
import unittest
from unittest.mock import patch, MagicMock
from app.delete_archives import delete_archive


class TestDeleteArchives(unittest.TestCase):

    @patch('app.delete_archives.CredentialManager')
    @patch('app.delete_archives.boto3.client')
    def test_delete_archive(self, mock_boto_client, mock_credential_manager):
        # Set up mock credentials
        mock_credentials = {
            'AccessKeyId': 'mock_key_id',
            'SecretAccessKey': 'mock_access_key',
            'SessionToken': 'mock_token'
        }
        mock_credential_manager.return_value.get_credentials.return_value = (
            mock_credentials
        )

        # Mock Glacier client behavior
        mock_glacier_client = MagicMock()
        mock_boto_client.return_value = mock_glacier_client

        delete_archive(
            'test_vault',
            'test_archive_id'
        )
        mock_glacier_client.delete_archive.assert_called_with(
            accountId='-',
            vaultName='test_vault',
            archiveId='test_archive_id'
        )


if __name__ == '__main__':
    unittest.main()
