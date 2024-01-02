import boto3
import time
from datetime import datetime, timedelta, timezone
import botocore
import logging
from typing import Dict, Optional


class CredentialManager:
    """
    Manages short-lived AWS credentials using STS (AWS Security Token Service).

    Attributes:
        session_duration (int): Duration for which the credentials are valid.
        credentials (Optional[Dict[str, str]]): Current AWS credentials.
        expiration (Optional[datetime]): Expiration time of current credentials.
        sts_client (boto3.client): Client for AWS STS.
    """

    def __init__(self, session_duration: int = 3600) -> None:
        """
        Initialize the Credential Manager with a session duration.
        Args:
            session_duration (int): Duration for which the credentials are valid.
        """
        self.logger = logging.getLogger(__name__)
        self.session_duration: int = session_duration
        self.credentials: Optional[Dict[str, str]] = None
        self.expiration: Optional[datetime] = None
        self.sts_client = boto3.client('sts')

    def get_credentials(self) -> Dict[str, str]:
        """
        Retrieves fresh credentials if the current ones are expired or about to expire.
        Returns:
            Dict[str, str]: AWS credentials (access key, secret key, session token).
        """
        if self._need_refresh():
            self._refresh_credentials()
        return self.credentials

    def get_glacier_client(self) -> boto3.client:
        """
        Creates and returns a Glacier client using the current credentials.
        Returns:
            boto3.client: A Glacier client.
        """
        self.get_credentials()  # Ensure credentials are up to date
        return boto3.client(
            'glacier',
            aws_access_key_id=self.credentials['AccessKeyId'],
            aws_secret_access_key=self.credentials['SecretAccessKey'],
            aws_session_token=self.credentials['SessionToken']
        )

    def _need_refresh(self) -> bool:
        """
        Determines if the AWS credentials need to be refreshed.
        Returns:
            bool: True if credentials need refresh, False otherwise.
        """
        now_utc = datetime.now(timezone.utc)
        return (not self.credentials or not self.expiration or
                now_utc >= self.expiration - timedelta(minutes=5))

    def _refresh_credentials(self, retries: int = 3, delay: int = 1) -> None:
        """
        Refreshes the AWS credentials with retry and exponential backoff strategy.
        Args:
            retries (int): Number of retry attempts.
            delay (int): Initial delay between retries in seconds.
        """
        for attempt in range(retries):
            try:
                response = self.sts_client.get_session_token(DurationSeconds=self.session_duration)
                self.credentials = response['Credentials']
                self.expiration = self.credentials['Expiration']
                break
            except botocore.exceptions.ClientError as error:
                if attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    self.logger.error(f"Failed to refresh credentials: {error}")
                    raise error
