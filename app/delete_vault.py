# app/delete_vault.py
import boto3
from app.credential_manager import CredentialManager


def delete_vault(vault_name):
    credential_manager = CredentialManager()

    def get_glacier_client():
        credentials = credential_manager.get_credentials()
        return boto3.client('glacier',
                            aws_access_key_id=credentials['AccessKeyId'],
                            aws_secret_access_key=credentials['SecretAccessKey'],
                            aws_session_token=credentials['SessionToken'])

    glacier_client = get_glacier_client()
    try:
        glacier_client.delete_vault(accountId='-', vaultName=vault_name)
        print(f"Deleted vault {vault_name}")
    except Exception as e:
        print(f"Failed to delete vault {vault_name}: {e}")
