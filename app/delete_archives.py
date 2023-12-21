# app/delete_archives.py
import boto3
from app.credential_manager import CredentialManager


def delete_archive(vault_name, archive_id):
    credential_manager = CredentialManager()

    def get_glacier_client():
        credentials = credential_manager.get_credentials()
        return boto3.client('glacier',
                            aws_access_key_id=credentials['AccessKeyId'],
                            aws_secret_access_key=credentials['SecretAccessKey'],
                            aws_session_token=credentials['SessionToken'])

    glacier_client = get_glacier_client()
    try:
        glacier_client.delete_archive(
            accountId='-', vaultName=vault_name, archiveId=archive_id)
        print(f"Deleted archive {archive_id} from vault {vault_name}")
    except Exception as e:
        print(f"Failed to delete archive {
              archive_id} from vault {vault_name}: {e}")
