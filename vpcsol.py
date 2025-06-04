import boto3
import json

def create_s3_gateway_endpoint():
    ec2 = boto3.client('ec2')
    
    vpc_id = 'vpc-0bb5e4b15fed04b22'
    subnet_id = 'subnet-0c70cfc7c3fcb10bd'
    region = boto3.Session().region_name or 'us-east-1'  # Replace with your region
    
    # Get the route table for the subnet
    print("Finding route table for subnet...")
    route_tables = ec2.describe_route_tables(
        Filters=[
            {'Name': 'association.subnet-id', 'Values': [subnet_id]}
        ]
    )
    
    if not route_tables['RouteTables']:
        print("No explicit association, using main route table...")
        route_tables = ec2.describe_route_tables(
            Filters=[
                {'Name': 'vpc-id', 'Values': [vpc_id]},
                {'Name': 'association.main', 'Values': ['true']}
            ]
        )
    
    route_table_id = route_tables['RouteTables'][0]['RouteTableId']
    print(f"Using route table: {route_table_id}")
    
    # Check if S3 gateway endpoint already exists
    existing_endpoints = ec2.describe_vpc_endpoints(
        Filters=[
            {'Name': 'vpc-id', 'Values': [vpc_id]},
            {'Name': 'service-name', 'Values': [f'com.amazonaws.{region}.s3']},
            {'Name': 'vpc-endpoint-type', 'Values': ['Gateway']}
        ]
    )
    
    if existing_endpoints['VpcEndpoints']:
        endpoint_id = existing_endpoints['VpcEndpoints'][0]['VpcEndpointId']
        print(f"S3 Gateway endpoint already exists: {endpoint_id}")
        
        # Check if it's associated with our route table
        associated_route_tables = existing_endpoints['VpcEndpoints'][0]['RouteTableIds']
        if route_table_id not in associated_route_tables:
            print(f"Adding route table {route_table_id} to existing endpoint...")
            try:
                ec2.modify_vpc_endpoint(
                    VpcEndpointId=endpoint_id,
                    AddRouteTableIds=[route_table_id]
                )
                print("✅ Route table added to existing endpoint!")
            except Exception as e:
                print(f"Error modifying endpoint: {e}")
        else:
            print("✅ Route table already associated with endpoint!")
        
        return endpoint_id
    
    # Create new S3 Gateway endpoint
    print("Creating new S3 Gateway endpoint...")
    
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket",
                    "s3:GetBucketLocation",
                    "s3:ListBucketMultipartUploads",
                    "s3:AbortMultipartUpload",
                    "s3:ListMultipartUploadParts"
                ],
                "Resource": "*"
            }
        ]
    }
    
    try:
        response = ec2.create_vpc_endpoint(
            VpcId=vpc_id,
            ServiceName=f'com.amazonaws.{region}.s3',
            VpcEndpointType='Gateway',  # This is crucial!
            RouteTableIds=[route_table_id],
            PolicyDocument=json.dumps(policy_document)
        )
        
        endpoint_id = response['VpcEndpoint']['VpcEndpointId']
        print(f"✅ S3 Gateway endpoint created: {endpoint_id}")
        print(f"Associated with route table: {route_table_id}")
        
        return endpoint_id
        
    except Exception as e:
        print(f"❌ Error creating VPC endpoint: {e}")
        return None

def verify_endpoint():
    """Verify the endpoint is working"""
    ec2 = boto3.client('ec2')
    vpc_id = 'vpc-0bb5e4b15fed04b22'
    region = boto3.Session().region_name or 'us-east-1'
    
    endpoints = ec2.describe_vpc_endpoints(
        Filters=[
            {'Name': 'vpc-id', 'Values': [vpc_id]},
            {'Name': 'service-name', 'Values': [f'com.amazonaws.{region}.s3']}
        ]
    )
    
    print("\n" + "="*50)
    print("VERIFICATION:")
    for endpoint in endpoints['VpcEndpoints']:
        print(f"Endpoint ID: {endpoint['VpcEndpointId']}")
        print(f"Type: {endpoint['VpcEndpointType']}")
        print(f"State: {endpoint['State']}")
        print(f"Route Tables: {endpoint.get('RouteTableIds', [])}")
        
        if endpoint['State'] == 'available':
            print("✅ Endpoint is ready!")
        else:
            print("⏳ Endpoint is still being created...")

# Create the endpoint
endpoint_id = create_s3_gateway_endpoint()

# Verify
if endpoint_id:
    verify_endpoint()