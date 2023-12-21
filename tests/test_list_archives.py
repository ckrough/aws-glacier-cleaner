# tests/test_list_archives.py
import unittest
from unittest.mock import patch, MagicMock
import json
from app.list_archives import list_archives

class TestListArchives(unittest.TestCase):

    @patch('app.list_archives.boto3.client')
    def test_list_archives(self, mock_client):
        # Mocking the AWS Glacier client responses
        mock_client.return_value.initiate_job.return_value = {'jobId': '123'}
        mock_client.return_value.describe_job.return_value = {'Completed': True}

        # Mocking the job output structure
        mock_job_output_content = json.dumps({
            'ArchiveList': [
                {'ArchiveId': 'archive1'},
                {'ArchiveId': 'archive2'}
            ]
        })

        # Mocking a file-like object for the 'body' attribute
        mock_body = MagicMock()
        mock_body.read.return_value = mock_job_output_content
        mock_client.return_value.get_job_output.return_value = {'body': mock_body}

        expected_archives = ['archive1', 'archive2']
        archives = list_archives('test_vault')
        self.assertEqual(archives, expected_archives)

if __name__ == '__main__':
    unittest.main()
