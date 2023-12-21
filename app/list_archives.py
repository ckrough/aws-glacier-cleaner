# app/list_archives.py
import boto3
import time
import json
import logging
from typing import List
from app.credential_manager import CredentialManager


def list_archives(vault_name: str) -> List[str]:
    """
    Lists all archives in a specified AWS Glacier vault.

    This function initiates an inventory retrieval job in the specified vault,
    polls for the job's completion, and then parses the job output to extract
    a list of archive IDs.

    Args:
        vault_name (str): The name of the AWS Glacier vault.

    Returns:
        List[str]: A list of archive IDs in the specified vault.
    """
    logger = logging.getLogger(__name__)
    credential_manager = CredentialManager()

    def get_glacier_client():
        """Fetches fresh credentials and returns a Glacier client."""
        credentials = credential_manager.get_credentials()
        return boto3.client(
            'glacier',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

    glacier_client = get_glacier_client()
    try:
        job_response = glacier_client.initiate_job(
            accountId='-',
            vaultName=vault_name,
            jobParameters={'Type': 'inventory-retrieval'}
        )
        job_id = job_response['jobId']
        logger.info(f"Inventory retrieval job started for vault {
                    vault_name}, Job ID: {job_id}")

        while True:
            glacier_client = get_glacier_client()  # Refresh client
            job_status = glacier_client.describe_job(
                accountId='-',
                vaultName=vault_name,
                jobId=job_id
            )

            if job_status['Completed']:
                job_output = glacier_client.get_job_output(
                    accountId='-',
                    vaultName=vault_name,
                    jobId=job_id
                )
                job_output_content = job_output['body'].read()

                inventory_data = json.loads(job_output_content)
                archives = [archive['ArchiveId']
                            for archive in inventory_data['ArchiveList']]
                return archives

            time.sleep(900)  # Poll every 15 minutes

    except Exception as e:
        logger.error(f"An error occurred while listing archives in vault {
                     vault_name}: {e}")
        return []
