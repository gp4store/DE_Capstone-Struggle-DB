#!/usr/bin/env python3

import boto3

def create_aurora_serverless_v2(cluster_name, username='admin'):
    """Create Aurora Serverless v2 with AWS Secrets Manager for password"""
    
    rds = boto3.client('rds')
    
    try:
        # Create the Aurora Serverless v2 cluster
        print(f"Creating Aurora Serverless v2 cluster: {cluster_name}")
        cluster_response = rds.create_db_cluster(
            DBClusterIdentifier=cluster_name,
            Engine='aurora-mysql',
            EnableHttpEndpoint= True, #Added this line on 05292025 to enable RDS data api
            PubliclyAccessible=True, #Added this line on 05292025 to enable Public Access
            MasterUsername=username,
            ManageMasterUserPassword=True,  # RDS manages the password
            MasterUserSecretKmsKeyId='alias/aws/secretsmanager',
            EngineMode='provisioned',  # Serverless v2 uses provisioned mode
            ServerlessV2ScalingConfiguration={
                'MinCapacity': 0.5,  # Minimum ACUs (can go lower than v1)
                'MaxCapacity': 4.0   # Maximum ACUs
            },
            BackupRetentionPeriod=7
        )
        
        print("Waiting for cluster to be ready...")
        
        # Wait for cluster to be available
        waiter = rds.get_waiter('db_cluster_available')
        waiter.wait(DBClusterIdentifier=cluster_name)
        
        # Create a serverless v2 DB instance
        instance_name = f"{cluster_name}-instance-1"
        print(f"Creating DB instance: {instance_name}")
        
        rds.create_db_instance(
            DBInstanceIdentifier=instance_name,
            DBClusterIdentifier=cluster_name,
            DBInstanceClass='db.serverless',  # Serverless v2 instance class
            Engine='aurora-mysql',
            PubliclyAccessible=False
        )
        
        print("Waiting for DB instance to be ready...")
        
        # Wait for instance to be available
        instance_waiter = rds.get_waiter('db_instance_available')
        instance_waiter.wait(DBInstanceIdentifier=instance_name)
        
        # Get cluster info
        cluster = rds.describe_db_clusters(DBClusterIdentifier=cluster_name)['DBClusters'][0]
        
        print(f"✅ Aurora Serverless v2 cluster created!")
        print(f"Cluster ID: {cluster['DBClusterIdentifier']}")
        print(f"Endpoint: {cluster['Endpoint']}")
        print(f"Reader Endpoint: {cluster.get('ReaderEndpoint', 'N/A')}")
        print(f"Port: {cluster['Port']}")
        print("\n💡 Find your database password in AWS Secrets Manager console")
        
        return cluster
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Usage
if __name__ == "__main__":
    create_aurora_serverless_v2("final-de-elca-struggle-db")