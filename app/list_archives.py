# app/list_archives.py
import boto3
import time
import json

def list_archives(vault_name):
    glacier_client = boto3.client('glacier')
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
