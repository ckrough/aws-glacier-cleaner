# app/glacier_vaults_list.py
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from typing import List, Union


def list_glacier_vaults() -> Union[List[str], str]:
    """
    Lists all the vault names in AWS Glacier for the given account.

    Returns:
        Union[List[str], str]: A list of vault names if successful, or an error message string.
    """
    try:
        client = boto3.client('glacier')
        response = client.list_vaults(accountId='-')
        vaults = response['VaultList']
        return [vault['VaultName'] for vault in vaults]
    except NoCredentialsError:
        return "No AWS credentials found"
    except ClientError as e:
        return str(e)
