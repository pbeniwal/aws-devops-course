# Create a function to create bucket with input as bucket name and region
import boto3

def create_bucket(bucket_name, region):
    s3_client = boto3.client('s3', region_name=region)
    if region == 'us-east-1':
        s3_client.create_bucket(Bucket=bucket_name)
    else:
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})

# Invoke this function with bucket name and region as input
if __name__ == "__main__":
    bucket_name = input("Enter the bucket name: ")
    region = input("Enter the region (e.g., us-west-1): ")
    create_bucket(bucket_name, region)
    print(f"Bucket '{bucket_name}' created in region '{region}'.")
    