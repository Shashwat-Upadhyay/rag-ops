"""Optional AWS extension: push the data + model index to S3 (and log to CloudWatch).
Usage:  python cloud/s3_sync.py upload   |   python cloud/s3_sync.py download
Needs: pip install boto3 ; `aws configure` ; env S3_BUCKET=your-bucket
NOTE: written to match the boto3 API but not tested against a real AWS account."""
import os
import sys
from pathlib import Path

import boto3

BUCKET = os.environ["S3_BUCKET"]
FOLDERS = ["data/raw", "data/index"]
s3 = boto3.client("s3")


def upload():
    for folder in FOLDERS:
        for p in Path(folder).rglob("*"):
            if p.is_file():
                s3.upload_file(str(p), BUCKET, f"ragops/{p.as_posix()}")
                print("uploaded", p)
    boto3.client("logs")  # CloudWatch client; see setup.md for the logging snippet


def download():
    for obj in s3.list_objects_v2(Bucket=BUCKET, Prefix="ragops/").get("Contents", []):
        target = Path(obj["Key"].removeprefix("ragops/"))
        target.parent.mkdir(parents=True, exist_ok=True)
        s3.download_file(BUCKET, obj["Key"], str(target))
        print("downloaded", target)


if __name__ == "__main__":
    {"upload": upload, "download": download}[sys.argv[1]]()
