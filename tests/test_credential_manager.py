import unittest
from unittest.mock import patch
from app.credential_manager import CredentialManager
from datetime import datetime, timedelta

class TestCredentialManager(unittest.TestCase):

    @patch('app.credential_manager.boto3.client')
    def test_get_credentials(self, mock_sts_client):
        fake_creds = {
            'AccessKeyId': 'AKIA...',
            'SecretAccessKey': 'SECRET...',
            'SessionToken': 'TOKEN...',
            'Expiration': datetime.utcnow() + timedelta(hours=1)
        }
        mock_sts_client.return_value.get_session_token.return_value = {'Credentials': fake_creds}

        manager = CredentialManager()
        credentials = manager.get_credentials()

        self.assertEqual(credentials['AccessKeyId'], 'AKIA...')
        self.assertEqual(credentials['SecretAccessKey'], 'SECRET...')
        self.assertEqual(credentials['SessionToken'], 'TOKEN...')

if __name__ == '__main__':
    unittest.main()
