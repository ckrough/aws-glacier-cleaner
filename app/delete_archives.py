# app/delete_archives.py
import boto3
from typing import NoReturn
from app.credential_manager import CredentialManager
import logging


def delete_archive(vault_name: str, archive_id: str) -> NoReturn:
    """
    Deletes a specific archive from an AWS Glacier vault.

    Args:
        vault_name (str): The name of the AWS Glacier vault.
        archive_id (str): The ID of the archive to be deleted.
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
        glacier_client.delete_archive(
            accountId='-',
            vaultName=vault_name,
            archiveId=archive_id
        )
        logger.info(f"Deleted archive {archive_id} from vault {vault_name}")
    except Exception as e:
        logger.error(f"Failed to delete archive {
                     archive_id} from vault {vault_name}: {e}")
