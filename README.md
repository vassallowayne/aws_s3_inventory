# aws_s3_inventory
Lists all AWS s3 buckets in all AWS profiles



## AWS S3 Buckets Inventory

This script automates the discovery and reporting of S3 buckets across multiple AWS accounts by leveraging locally configured AWS CLI profiles.

### What It Does

- Connects to AWS accounts using profiles defined in `~/.aws/credentials` and `~/.aws/config`.
- For each profile, it retrieves:
  - The AWS account ID via STS
  - The list of all S3 buckets
- Outputs the results into a CSV file, including:
  - AWS account name (profile)
  - AWS account ID
  - S3 bucket name

### Requirements

- Python 3.x
- boto3 and botocore (`pip install boto3`)
- AWS CLI profiles properly configured under your user account
- 'credentials' file updated with creds for AWS profiles required

### Usage

Scan specific profiles:
```bash
python aws_s3_inventory.py --profiles default,prod,dev
