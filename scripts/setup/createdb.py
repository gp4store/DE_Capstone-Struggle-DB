
import boto3
from botocore.exceptions import ClientError

def create_glue_database():

    glue_client = boto3.client('glue', region_name='us-west-1')
    database_name = 'your-database-name'
    response = glue_client.create_database(
        DatabaseInput={
            'Name': database_name,
            'Description': 'Simple data lake database for analytics'
        }
    )
    
    print(f"Database '{database_name}' created successfully!")
    return True

if __name__ == "__main__":
    print("Creating AWS Glue Database...")
    create_glue_database()