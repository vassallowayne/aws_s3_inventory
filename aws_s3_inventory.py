# Author: Wayne Vassallo

import boto3
import botocore
import argparse
import sys
import csv
import os
import configparser


def get_available_profiles():
    config_path = os.path.expanduser("~/.aws/config")
    config = configparser.ConfigParser()
    config.read(config_path)

    profiles = []
    for section in config.sections():
        if section.startswith("profile "):
            profiles.append(section.split("profile ")[1])
    return profiles


def main():
    parser = argparse.ArgumentParser(description="Generate AWS S3 Bucket report")
    parser.add_argument('--profiles', help="Comma-separated AWS profiles to use", dest='profiles',
                        default=None)
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    parser.set_defaults(verbose=True)
    args = parser.parse_args()

    if args.profiles:
        profile_list = [p.strip() for p in args.profiles.split(',')]
    else:
        profile_list = get_available_profiles()

    if args.verbose:
        print(f"Using profiles: {profile_list}", file=sys.stderr)

    csv_lines = []
    csv_fields = []

    for profile in profile_list:
        try:
            session = boto3.Session(profile_name=profile)
            sts = session.client("sts")
            identity = sts.get_caller_identity()
            account_id = identity['Account']
            account_name = profile

            if args.verbose:
                print(f"Querying profile {profile} (Account ID: {account_id})", file=sys.stderr)

            s3 = session.client("s3", region_name="us-east-1")
            buckets = s3.list_buckets()

            for bucket in buckets['Buckets']:
                entry = {
                    'aws_accountName': account_name,
                    'aws_accountId': account_id,
                    's3_bucketName': bucket['Name']
                }
                csv_lines.append(entry)
                csv_fields = list(set(csv_fields + list(entry.keys())))

        except botocore.exceptions.ClientError as e:
            print(f"[!] Error with profile {profile}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"[!] Unexpected error with profile {profile}: {e}", file=sys.stderr)

    if csv_lines:
        filename = "aws_s3_buckets_inventory.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[n for n in csv_fields], dialect=csv.excel)
            writer.writeheader()
            writer.writerows(csv_lines)
        print(f"[+] CSV file '{filename}' created successfully.")
    else:
        print("[!] No data to write.")


if __name__ == "__main__":
    main()
