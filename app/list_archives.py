# app/list_archives.py
import boto3
import time
import json
from app.credential_manager import CredentialManager

# Add relevant imports and use CredentialManager to get credentials

def list_archives(vault_name):
    credential_manager = CredentialManager()
    credentials = credential_manager.get_credentials()

    glacier_client = boto3.client('glacier', 
                                  aws_access_key_id=credentials['AccessKeyId'],
                                  aws_secret_access_key=credentials['SecretAccessKey'],
                                  aws_session_token=credentials['SessionToken'])

    # Start an inventory-retrieval job
    job_response = glacier_client.initiate_job(
        accountId='-',
        vaultName=vault_name,
        jobParameters={'Type': 'inventory-retrieval'}
    )
    job_id = job_response['jobId']
    print(f"Inventory retrieval job started for vault {vault_name}, Job ID: {job_id}")

    # Polling for job completion
    while True:
        job_status = glacier_client.describe_job(accountId='-', vaultName=vault_name, jobId=job_id)
        if job_status['Completed']:
            print(f"Job completed for vault {vault_name}")
            break
        time.sleep(900)  # Poll every hour

    # Retrieve job output
    job_output = glacier_client.get_job_output(accountId='-', vaultName=vault_name, jobId=job_id)
    job_output_content = job_output['body'].read()

    # Parse the job output to extract archive list
    try:
        inventory_data = json.loads(job_output_content)
        archives = [archive['ArchiveId'] for archive in inventory_data['ArchiveList']]
        return archives
    except json.JSONDecodeError:
        print("Error parsing job output")
        return []

    return []
