"""Optional AWS extension: run the pipeline as a SageMaker *training job* (managed container, pay per second).
Usage: python cloud/sagemaker_train.py   (needs `pip install sagemaker`, an execution role in SAGEMAKER_ROLE, S3_BUCKET)
NOTE: not tested against a real AWS account. Run cloud/teardown.py afterwards."""
import os

from sagemaker.sklearn.estimator import SKLearn

est = SKLearn(
    entry_point="cloud/sagemaker_entry.py", source_dir=".", framework_version="1.2-1", py_version="py3",
    role=os.environ["SAGEMAKER_ROLE"], instance_type="ml.m5.large", instance_count=1,
    max_run=1800,                                   # hard stop after 30 min to cap cost
    output_path=f"s3://{os.environ['S3_BUCKET']}/ragops/sagemaker-output",
    dependencies=["requirements.txt"],
)
est.fit(wait=True)                                   # logs stream to CloudWatch automatically
print("Model artifacts:", est.model_data)
