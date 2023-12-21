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

    glacier_client = credential_manager.get_glacier_client()

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
