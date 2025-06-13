
import boto3
import logging
from botocore.exceptions import ClientError

def create_s3_bucket(bucket_name, region='us-west-1'):
    """
    Create an S3 bucket in a specified region
    
    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-1'
    :return: True if bucket was created, else False
    """
    try:
        s3_client = boto3.client('s3', region_name=region)
        
        if region == 'us-east-1':
           
            s3_client.create_bucket(Bucket=bucket_name)
        else:
           
            location = {'LocationConstraint': region}
            s3_client.create_bucket(
                Bucket=bucket_name, 
                CreateBucketConfiguration=location
            )
        
        logging.info(f"Bucket '{bucket_name}' created successfully in region '{region}'")
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyExists':
            logging.error(f"Bucket '{bucket_name}' already exists")
        elif error_code == 'BucketAlreadyOwnedByYou':
            logging.warning(f"Bucket '{bucket_name}' already owned by you")
            return True
        else:
            logging.error(f"Error creating bucket: {e}")
        return False
    
    return True

if __name__ == "__main__":
   
    logging.basicConfig(level=logging.INFO)
    
    bucket_name = 'your-bucket-processed'
    region = 'us-west-1'
    
    if create_s3_bucket(bucket_name, region):
        print(f"Successfully created bucket: {bucket_name}")
    else:
        print(f"Failed to create bucket: {bucket_name}")