#!/usr/bin/env python3

import boto3
import logging
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

def create_s3_bucket(bucket_name, region='us-east-1'):

    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":

    bucket_name = 'de-elca-capstone-gp'
