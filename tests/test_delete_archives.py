# tests/test_delete_archives.py
import unittest
from unittest.mock import patch
from app.delete_archives import delete_archive

class TestDeleteArchives(unittest.TestCase):

    @patch('app.delete_archives.boto3.client')
    def test_delete_archive(self, mock_client):
        delete_archive('test_vault', 'test_archive_id')
        mock_client.return_value.delete_archive.assert_called_with(
            accountId='-',
            vaultName='test_vault',
            archiveId='test_archive_id'
        )

if __name__ == '__main__':
    unittest.main()
