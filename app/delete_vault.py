# app/delete_vault.py
import boto3

def delete_vault(vault_name):
    glacier_client = boto3.client('glacier')
    try:
        glacier_client.delete_vault(accountId='-', vaultName=vault_name)
        return True
    except Exception as e:
        print(f"Failed to delete vault {vault_name}: {e}")
        return False
