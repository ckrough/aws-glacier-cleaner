# AWS Glacier Vault Cleaner

## Overview

The **AWS Glacier Vault Cleaner** is designed to identify and delete all
Amazon Web Services (AWS) Glacier Archives and Vaults within an AWS Account.
This tool is intended for bulk cleanup of AWS Glacier Vaults and should be 
used with caution.

### Warning

**This application will DELETE ALL archives and vaults in the specified AWS 
account without user interaction or warning.**
Use this tool ONLY if you intend to remove all data stored in AWS 
Glacier Vaults. Ensure you have backups or have migrated your data elsewhere 
if necessary, as this process is irreversible.

## Features

- **Bulk Deletion**: Automatically identifies and deletes all Glacier Archives and 
  Vaults in an AWS account.

- **Credential Management**: Utilizes the AWS Security Token Service (STS) 
  to manage credentials securely. The application dynamically refreshes 
  short-lived credentials, ensuring consistent and secure access to AWS 
  services throughout the duration of long-running jobs.

## Intention

This tool is specifically designed for scenarios where a complete cleanup of 
AWS Glacier Vaults is required. It is particularly useful for development, 
testing, or other environments where bulk deletion of data is a frequent 
necessity.

## Prerequisites

- **Python 3**: The application is written in Python 3 and requires a Python 3 
  environment to run.
- **AWS Account**: You must have an AWS account with access to the Glacier 
  service. [AWS Glacier Documentation](https://docs.aws.amazon.com/amazonglacier/latest/dev/introduction.html)
- **AWS Credentials**: Properly configured AWS credentials with access rights 
  to AWS Glacier are necessary. [Managing AWS Credentials](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html)
- **Dependencies**: The application depends on several Python packages such as 
  `boto3`, `botocore`, and `python-dateutil`. Install these via `pip`.

## Installation

Clone the repository and install the required Python packages:

```
git clone <repository-url>
cd <repository-directory>
pip install -r requirements.txt
```

## Usage

Before running the application, **ensure your AWS credentials are configured 
correctly** and you understand the implications of using this tool. The 
application can be executed from the command line as follows:

```
python glacier_vault_cleaner.py
```

## Contributing

Contributions to the AWS Glacier Vault Cleaner are welcome. Please ensure that 
your code adheres to the project's coding standards and includes tests for new 
features.

## License

MIT License

Copyright (c) [2023] [Chris Krough]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
