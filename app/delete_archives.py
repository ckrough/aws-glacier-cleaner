# app/delete_archives.py
import boto3
from app.credential_manager import CredentialManager

def delete_archive(vault_name, archive_id):
    glacier_client = boto3.client('glacier')
    glacier_client.delete_archive(accountId='-', vaultName=vault_name, archiveId=archive_id)
    print(f"Deleted archive {archive_id} from vault {vault_name}")
