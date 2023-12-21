# app/glacier_vaults_list.py
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


def list_glacier_vaults():
    try:
        client = boto3.client('glacier')
        response = client.list_vaults(accountId='-')
        vaults = response['VaultList']
        return [vault['VaultName'] for vault in vaults]
    except NoCredentialsError:
        return "No AWS credentials found"
    except ClientError as e:
        return str(e)
