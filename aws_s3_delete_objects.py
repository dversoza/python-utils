import os
import sys
import boto3

# Create an AWS session using the default profile
aws_session = boto3.Session(profile_name=os.environ.get("AWS_PROFILE"))
s3_client = aws_session.client("s3")


def list_objects(bucket_name, next_token=None):
    # List all objects in the specified S3 bucket
    if next_token:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name, ContinuationToken=next_token
        )
    else:
        response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Check if the bucket is empty
    if "Contents" not in response:
        print(f"The bucket {bucket_name} is empty.")
        return

    # Iterate through all the objects in the bucket
    for obj in response["Contents"]:
        yield obj["Key"]

    # Check if there are more objects to list
    if "NextContinuationToken" in response:
        next_token = response["NextContinuationToken"]
        yield from list_objects(bucket_name, next_token)


def delete_objects(bucket_name, pattern):
    # List all objects in the specified S3 bucket
    for key in list_objects(bucket_name):
        # Check if the object key contains the specified pattern
        if pattern in key:
            print(f"Deleting {key}...")
            s3_client.delete_object(Bucket=bucket_name, Key=key)

    print(f"All objects containing {pattern} have been deleted.")


if __name__ == "__main__":
    args = sys.argv[1:]

    bucket_name = args[0]
    pattern = args[1]

    delete_objects(bucket_name, pattern)
