import boto3
from datetime import datetime, timedelta
from typing import Dict, Optional


class CredentialManager:
    """
    Manages short-lived AWS credentials using STS (AWS Security Token Service).

    Attributes:
        session_duration (int): The duration for which the credentials are
        valid (in seconds).
        credentials (dict, optional): The current AWS credentials.
        expiration (datetime, optional): The expiration time of the current
            credentials.
        sts_client (boto3.client): The client for AWS STS.
    """

    def __init__(self, session_duration: int = 3600) -> None:
        """
        Initialize the Credential Manager with a specified session duration.

        Args:
            session_duration (int): The duration for which the credentials are
            valid (in seconds).
        """
        self.session_duration: int = session_duration
        self.credentials: Optional[Dict[str, str]] = None
        self.expiration: Optional[datetime] = None
        self.sts_client = boto3.client('sts')

    def get_credentials(self) -> Dict[str, str]:
        """
        Retrieves fresh credentials if the current ones are expired or about
        to expire.

        Returns:
            Dict[str, str]: AWS credentials including access key, secret key,
            and session token.
        """
        if not self.credentials or self._are_credentials_expired():
            self._refresh_credentials()
        return self.credentials

    def _refresh_credentials(self) -> None:
        """
        Refreshes the AWS credentials by fetching a new set from AWS STS.
        """
        response = self.sts_client.get_session_token(
            DurationSeconds=self.session_duration)
        self.credentials = response['Credentials']
        self.expiration = self.credentials['Expiration']

    def _are_credentials_expired(self) -> bool:
        """
        Checks if the current credentials are expired or about to expire.

        Returns:
            bool: True if credentials are expired or about to expire,
            False otherwise.
        """
        return (
            not self.expiration or 
            self.expiration - datetime.utcnow() < timedelta(minutes=5)
        )
