import boto3

def check_vpc_endpoint_status():
    ec2 = boto3.client('ec2')
    
    vpc_id = 'vpc-0bb5e4b15fed04b22'
    subnet_id = 'subnet-0c70cfc7c3fcb10bd'
    region = boto3.Session().region_name or 'us-east-1'  # Replace with your region
    
    print(f"Checking VPC: {vpc_id}")
    print(f"Checking Subnet: {subnet_id}")
    print(f"Region: {region}")
    print("-" * 50)
    
    # 1. Check existing S3 VPC endpoints
    print("1. Existing S3 VPC Endpoints:")
    endpoints = ec2.describe_vpc_endpoints(
        Filters=[
            {'Name': 'vpc-id', 'Values': [vpc_id]},
            {'Name': 'service-name', 'Values': [f'com.amazonaws.{region}.s3']}
        ]
    )
    
    if endpoints['VpcEndpoints']:
        for endpoint in endpoints['VpcEndpoints']:
            print(f"   Endpoint ID: {endpoint['VpcEndpointId']}")
            print(f"   State: {endpoint['State']}")
            print(f"   Route Tables: {endpoint.get('RouteTableIds', [])}")
    else:
        print("   No S3 VPC endpoints found!")
    
    print()
    
    # 2. Check subnet's route table
    print("2. Subnet Route Table:")
    route_tables = ec2.describe_route_tables(
        Filters=[
            {'Name': 'association.subnet-id', 'Values': [subnet_id]}
        ]
    )
    
    if not route_tables['RouteTables']:
        print("   No explicit association found, checking main route table...")
        route_tables = ec2.describe_route_tables(
            Filters=[
                {'Name': 'vpc-id', 'Values': [vpc_id]},
                {'Name': 'association.main', 'Values': ['true']}
            ]
        )
    
    for rt in route_tables['RouteTables']:
        print(f"   Route Table ID: {rt['RouteTableId']}")
        print("   Routes:")
        for route in rt['Routes']:
            dest = route.get('DestinationCidrBlock') or route.get('DestinationPrefixListId', 'Unknown')
            target = (route.get('GatewayId') or 
                     route.get('VpcEndpointId') or 
                     route.get('NatGatewayId') or 
                     route.get('InstanceId') or 'local')
            print(f"     {dest} -> {target}")
    
    print()
    
    # 3. Check if subnet is public or private
    print("3. Subnet Analysis:")
    subnets = ec2.describe_subnets(SubnetIds=[subnet_id])
    subnet = subnets['Subnets'][0]
    
    print(f"   Subnet ID: {subnet['SubnetId']}")
    print(f"   AZ: {subnet['AvailabilityZone']}")
    print(f"   CIDR: {subnet['CidrBlock']}")
    
    # Check if it has internet gateway route
    has_igw = any(route.get('GatewayId', '').startswith('igw-') 
                  for rt in route_tables['RouteTables'] 
                  for route in rt['Routes'])
    
    has_nat = any(route.get('NatGatewayId', '').startswith('nat-') 
                  for rt in route_tables['RouteTables'] 
                  for route in rt['Routes'])
    
    has_s3_endpoint = any(route.get('GatewayId', '').startswith('vpce-') 
                         for rt in route_tables['RouteTables'] 
                         for route in rt['Routes'])
    
    print(f"   Has Internet Gateway: {has_igw}")
    print(f"   Has NAT Gateway: {has_nat}")
    print(f"   Has S3 VPC Endpoint: {has_s3_endpoint}")
    
    if not (has_igw or has_nat or has_s3_endpoint):
        print("   ❌ PROBLEM: Subnet has no route to internet or S3!")
    
    return route_tables['RouteTables'][0]['RouteTableId'] if route_tables['RouteTables'] else None

# Run the check
route_table_id = check_vpc_endpoint_status()