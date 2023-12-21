import boto3
from datetime import datetime, timedelta

class CredentialManager:
    """
    Manages short-lived AWS credentials using STS.
    """

    def __init__(self, session_duration=3600):
        """
        Initialize the Credential Manager with a specified session duration.

        Args:
            session_duration (int): The duration for which the credentials are valid (in seconds).
        """
        self.session_duration = session_duration
        self.credentials = None
        self.expiration = None
        self.sts_client = boto3.client('sts')

    def get_credentials(self):
        """
        Retrieves fresh credentials if the current ones are expired or about to expire.

        Returns:
            dict: AWS credentials
        """
        if not self.credentials or self._are_credentials_expired():
            self._refresh_credentials()
        return self.credentials

    def _refresh_credentials(self):
        """
        Refreshes the AWS credentials.
        """
        response = self.sts_client.get_session_token(DurationSeconds=self.session_duration)
        self.credentials = response['Credentials']
        self.expiration = self.credentials['Expiration']

    def _are_credentials_expired(self):
        """
        Checks if the current credentials are expired or about to expire.

        Returns:
            bool: True if credentials are expired or about to expire, False otherwise.
        """
        return not self.expiration or self.expiration - datetime.utcnow() < timedelta(minutes=5)

# Example usage:
# credential_manager = CredentialManager()
# credentials = credential_manager.get_credentials()
# glacier_client = boto3.client('glacier', aws_access_key_id=credentials['AccessKeyId'],
#                               aws_secret_access_key=credentials['SecretAccessKey'],
#                               aws_session_token=credentials['SessionToken'])
