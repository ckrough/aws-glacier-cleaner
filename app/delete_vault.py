# app/delete_vault.py
import boto3
from typing import NoReturn
from app.credential_manager import CredentialManager
import logging


def delete_vault(vault_name: str) -> NoReturn:
    """
    Deletes an AWS Glacier vault.

    Args:
        vault_name (str): The name of the AWS Glacier vault to be deleted.
    """
    logger = logging.getLogger(__name__)
    credential_manager = CredentialManager()

    def get_glacier_client():
        """
        Creates and returns a Glacier client using fresh credentials.

        Returns:
            boto3.client: A Glacier client.
        """
        credentials = credential_manager.get_credentials()
        return boto3.client(
            'glacier',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

    glacier_client = get_glacier_client()
    try:
        glacier_client.delete_vault(accountId='-', vaultName=vault_name)
        logger.info(f"Deleted vault {vault_name}")
    except Exception as e:
        logger.error(f"Failed to delete vault {vault_name}: {e}")
