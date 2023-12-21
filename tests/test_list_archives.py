# tests/test_list_archives.py
import unittest
from unittest.mock import patch, MagicMock
import json
from app.list_archives import list_archives


class TestListArchives(unittest.TestCase):

    @patch('app.list_archives.logging.getLogger')
    @patch('app.list_archives.CredentialManager.get_glacier_client')
    def test_list_archives(self, mock_get_glacier_client, mock_logger):
        mock_logger.return_value = MagicMock()

        # Mock Glacier client and its methods
        mock_glacier_client = MagicMock()
        mock_get_glacier_client.return_value = mock_glacier_client
        mock_glacier_client.initiate_job.return_value = {'jobId': '123'}
        mock_glacier_client.describe_job.return_value = {'Completed': True}
        mock_job_output = {
            'body': MagicMock(read=lambda: json.dumps({
                'ArchiveList': [
                    {'ArchiveId': 'archive1'},
                    {'ArchiveId': 'archive2'}
                ]
            }))
        }
        mock_glacier_client.get_job_output.return_value = mock_job_output

        archives = list_archives('test_vault')
        self.assertEqual(archives, ['archive1', 'archive2'])


if __name__ == '__main__':
    unittest.main()
