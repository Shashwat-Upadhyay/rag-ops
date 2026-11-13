"""Delete cloud resources after the demo to avoid cost. Usage: S3_BUCKET=my-bucket python cloud/teardown.py"""
import os

import boto3

bucket = boto3.resource("s3").Bucket(os.environ["S3_BUCKET"])
bucket.objects.filter(Prefix="ragops/").delete()
print("Deleted s3://%s/ragops/*" % bucket.name)
sm = boto3.client("sagemaker")
for e in sm.list_endpoints()["Endpoints"]:
    if e["EndpointName"].startswith("ragops"):
        sm.delete_endpoint(EndpointName=e["EndpointName"])
        print("Deleted endpoint", e["EndpointName"])
print("Also delete the bucket itself and the CloudWatch log group /aws/sagemaker/TrainingJobs if you created them.")
