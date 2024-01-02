import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
import botocore
from app.credential_manager import CredentialManager


class TestCredentialManager(unittest.TestCase):

    @patch('app.credential_manager.boto3.client')
    def setUp(self, mock_boto_client):
        self.mock_sts_client = MagicMock()
        mock_boto_client.return_value = self.mock_sts_client
        self.manager = CredentialManager()

    def test_get_credentials_success(self):
        """Test successful retrieval of credentials."""
        fake_credentials = {
            'AccessKeyId': 'AKIA...',
            'SecretAccessKey': '...',
            'SessionToken': '...',
            'Expiration': datetime.now(timezone.utc) + timedelta(hours=1)
        }
        self.mock_sts_client.get_session_token.return_value = {'Credentials': fake_credentials}
        
        credentials = self.manager.get_credentials()
        self.assertIsNotNone(credentials)
        self.assertEqual(credentials['AccessKeyId'], 'AKIA...')

    def test_get_credentials_with_refresh(self):
        """Test credential refresh when they are expired."""
        expired_credentials = {
            'AccessKeyId': 'AKIA...',
            'SecretAccessKey': '...',
            'SessionToken': '...',
            'Expiration': datetime.now(timezone.utc) - timedelta(minutes=10)
        }
        new_credentials = {
            'AccessKeyId': 'AKIA...NEW',
            'SecretAccessKey': '...NEW',
            'SessionToken': '...NEW',
            'Expiration': datetime.now(timezone.utc) + timedelta(hours=1)
        }

        # Set initial expired credentials
        self.manager.credentials = expired_credentials
        self.manager.expiration = expired_credentials['Expiration']

        # Mock STS client to return new credentials
        self.mock_sts_client.get_session_token.return_value = {'Credentials': new_credentials}

        credentials = self.manager.get_credentials()
        self.assertEqual(credentials['AccessKeyId'], 'AKIA...NEW')

    def test_get_credentials_with_failed_refresh(self):
        """Test failed credential refresh."""
        self.mock_sts_client.get_session_token.side_effect = botocore.exceptions.ClientError(
            {'Error': {}}, 'get_session_token')

        with self.assertRaises(botocore.exceptions.ClientError):
            self.manager.get_credentials()

    def test_retry_logic_in_refresh_credentials(self):
        """Test retry logic in credential refresh."""
        self.mock_sts_client.get_session_token.side_effect = [
            botocore.exceptions.ClientError({'Error': {}}, 'get_session_token'),
            {'Credentials': {
                'AccessKeyId': 'AKIA...RETRY',
                'SecretAccessKey': '...RETRY',
                'SessionToken': '...RETRY',
                'Expiration': datetime.now(timezone.utc) + timedelta(hours=1)
            }}
        ]

        credentials = self.manager.get_credentials()
        self.assertEqual(credentials['AccessKeyId'], 'AKIA...RETRY')


if __name__ == '__main__':
    unittest.main()
