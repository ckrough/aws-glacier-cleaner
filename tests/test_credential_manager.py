# tests/test_credential_manager.py
import unittest
from unittest.mock import patch, MagicMock
from app.credential_manager import CredentialManager


class TestCredentialManager(unittest.TestCase):

    @patch('app.credential_manager.boto3.client')
    @patch('app.credential_manager.logging.getLogger')
    def test_get_credentials(self, mock_logger, mock_boto_client):
        # Mock logging
        mock_logger.return_value = MagicMock()

        # Mock boto3 STS client response
        mock_sts_client = MagicMock()
        mock_boto_client.return_value = mock_sts_client
        mock_sts_client.get_session_token.return_value = {
            'Credentials': {
                'AccessKeyId': 'AKIA...',
                'SecretAccessKey': 'SECRET...',
                'SessionToken': 'TOKEN...',
                'Expiration': '2023-01-01T00:00:00Z'
            }
        }

        manager = CredentialManager()
        credentials = manager.get_credentials()

        self.assertEqual(credentials['AccessKeyId'], 'AKIA...')
        self.assertEqual(credentials['SecretAccessKey'], 'SECRET...')
        self.assertEqual(credentials['SessionToken'], 'TOKEN...')

        # Test for exception handling in get_credentials
        mock_sts_client.get_session_token.side_effect = Exception("Error")
        with self.assertRaises(Exception):
            manager.get_credentials()
            mock_logger.error.assert_called_with(
                "Error refreshing credentials: Error")


if __name__ == '__main__':
    unittest.main()
