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

    glacier_client = credential_manager.get_glacier_client()

    try:
        glacier_client.delete_vault(accountId='-', vaultName=vault_name)
        logger.info(f"Deleted vault {vault_name}")
    except Exception as e:
        logger.error(f"Failed to delete vault {vault_name}: {e}")
