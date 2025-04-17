import os
import json
import boto3
import io
import uuid
from dotenv import load_dotenv

def load_env_variables():
    load_dotenv()
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "s3_bucket_name": os.getenv("S3_BUCKET_NAME"),
    }

def make_s3_client():
    # Load AWS credentials from .env
    aws_credentials = load_env_variables()

    # Validate required environment variables
    if not aws_credentials["aws_access_key_id"]:
        raise ValueError("No AWS Access key id set")
    if not aws_credentials["aws_secret_access_key"]:
        raise ValueError("No AWS Secret Access key set")
    if not aws_credentials["aws_region"]:
        raise ValueError("No AWS Region Set")
    if not aws_credentials["s3_bucket_name"]:
        raise ValueError("S3_BUCKET_NAME environment variable is not set")

    # Using the boto3 library, initialize S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_credentials["aws_access_key_id"],
        aws_secret_access_key=aws_credentials["aws_secret_access_key"],
        region_name=aws_credentials["aws_region"],
    )

    return s3_client

def upload_obj_to_s3(payload):
    file_name_id = uuid.uuid4()
    file_name = f'{file_name_id}.json'
    aws_credentials = load_env_variables()

    s3_client = make_s3_client()
    
    json_bytes = io.BytesIO()
    json_bytes.write(json.dumps(payload).encode('utf-8'))
    json_bytes.seek(0)

    s3_client.upload_fileobj(
        json_bytes,
        aws_credentials["s3_bucket_name"],
        file_name
    )