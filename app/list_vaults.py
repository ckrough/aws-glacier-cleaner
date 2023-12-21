# app/list_vaults.py
from typing import List, Union
import logging
from botocore.exceptions import NoCredentialsError, ClientError
from app.credential_manager import CredentialManager


def list_vaults() -> Union[List[str], str]:
    """
    Lists all the vault names in AWS Glacier for the given account.

    Uses CredentialManager to get a Glacier client and lists the vaults. 
    Handles specific AWS client-related exceptions and logs errors.

    Returns:
        Union[List[str], str]: List of vault names if successful, or 
        an error message string in case of failure.
    """
    logger = logging.getLogger(__name__)
    credential_manager = CredentialManager()

    try:
        glacier_client = credential_manager.get_glacier_client()
        response = glacier_client.list_vaults(accountId='-')
        vaults = response['VaultList']
        return [vault['VaultName'] for vault in vaults]
    except NoCredentialsError:
        message = "No AWS credentials found"
        logger.error(message)
        return message
    except ClientError as e:
        message = f"Client error occurred: {e}"
        logger.error(message)
        return message
