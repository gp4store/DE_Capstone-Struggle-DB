import boto3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_glue_crawler():
    """Create a simple AWS Glue crawler for S3"""
    
    # Initialize Glue client
    glue_client = boto3.client('glue')
    
    # Crawler configuration
    crawler_name = 'sales_transaction_crawler'
    s3_path = 's3://source-raw-data-app/sales_transactions'  # Replace with your S3 path
    database_name = 'struggle_db'  # Replace with your database name
    iam_role = 'arn:aws:iam::248189910447:role/struggle-db-glue-permissions'  # Replace with your IAM role
    
    try:
        response = glue_client.create_crawler(
            Name=crawler_name,
            Role=iam_role,
            DatabaseName=database_name,
            Targets={
                'S3Targets': [
                    {
                        'Path': s3_path
                    }
                ]
            },
            Description='Simple S3 crawler',
            Configuration='{"Version": 1, "CreatePartitionIndex": true, "Grouping": {"TableGroupingPolicy": "CombineCompatibleSchemas"}}',
            SchemaChangePolicy={
                'UpdateBehavior': 'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'DEPRECATE_IN_DATABASE'
            }
        )
        
        logger.info(f"Crawler '{crawler_name}' created successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error creating crawler: {str(e)}")
        raise

if __name__ == "__main__":
    # Create the crawler
    create_glue_crawler()

