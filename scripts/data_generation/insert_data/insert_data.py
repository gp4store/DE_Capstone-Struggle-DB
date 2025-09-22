import boto3
import json
from faker import Faker
from datetime import datetime
import random

fake = Faker()
rds_client = boto3.client('rds-data', region_name='us-west-1')
cluster_arn = 'your-aurora-cluster-arn'
secret_arn = 'your-aws-secret-arn'
database_name = 'your-database-name'

def format_parameter(key, value):
    """Convert Python value to RDS Data API parameter format"""
    if isinstance(value, str):
        return {'name': key, 'value': {'stringValue': value}}
    elif isinstance(value, int):
        return {'name': key, 'value': {'longValue': value}}
    elif isinstance(value, float):
        return {'name': key, 'value': {'doubleValue': value}}
    elif isinstance(value, bool):
        return {'name': key, 'value': {'booleanValue': value}}
    elif isinstance(value, datetime):
        return {'name': key, 'value': {'stringValue': value.isoformat()}}
    elif value is None:
        return {'name': key, 'value': {'isNull': True}}
    else:
        return {'name': key, 'value': {'stringValue': str(value)}}

def execute_query(sql, parameters=None):
    """Execute a single SQL query"""
    try:
        params = {
            'resourceArn': cluster_arn,
            'secretArn': secret_arn,
            'database': database_name,
            'sql': sql
        }
        if parameters:
            params['parameters'] = parameters
            
        response = rds_client.execute_statement(**params)
        return response
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return None

def insert_batch_records(table_name, records):
    """Insert multiple records using batch operation"""
    if not records:
        return None
    
    columns = ', '.join(records[0].keys())
    placeholders = ', '.join([f':{key}' for key in records[0].keys()])
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    parameter_sets = []
    for record in records:
        parameters = [format_parameter(key, value) for key, value in record.items()]
        parameter_sets.append(parameters)
    
    try:
        response = rds_client.batch_execute_statement(
            resourceArn=cluster_arn,
            secretArn=secret_arn,
            database=database_name,
            sql=sql,
            parameterSets=parameter_sets
        )
        print(f"Batch insert completed: {len(records)} records inserted into {table_name}")
        return response
    except Exception as e:
        print(f"Error in batch insert: {str(e)}")
        return None

def get_existing_ids(table_name, id_column):
    """Fetch existing IDs from a table"""
    sql = f"SELECT {id_column} FROM {table_name}"
    response = execute_query(sql)
    
    if response and 'records' in response:
        ids = [record[0]['longValue'] for record in response['records']]
        return ids
    return []

def clear_tables():
    """Clear all tables in proper order (respecting foreign keys)"""
    print("Clearing existing data...")
    execute_query("DELETE FROM sales_transaction")
    execute_query("DELETE FROM product") 
    execute_query("DELETE FROM customers")
    print("Tables cleared.")

def generate_user_data():
    """Generate fake user data - without customer_id (let DB auto-increment)"""
    return {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'registration_date': fake.date_time_between(start_date='-2y', end_date='now'),
        'loyalty_points': fake.random_int(min=0, max=10000)
    }

def generate_product_data():
    """Generate fake product data - without product_id (let DB auto-increment)"""
    style = ['top unisex', 'center unisex', 'shorts for men', 'shirt for men', 'long sleeve shirt', 
             'pants', 'socks', 'shirt for girl', 'shorts for girl']
    size = ['small', 'medium', 'large', 'extra large', '2XL']
    brands = ['Nike', 'Adidas', 'Puma', 'Under Armour', 'H&M', 'Zara', 'Uniqlo', 'Gap', 'Levi\'s']
    items = ["Running Shorts", "Athletic Tank Top", "Compression Leggings", "Basketball Jersey", "Soccer Cleats", "Tennis Skirt", 
             "Workout Hoodie", "Running Shoes", "Sports Bra", "Track Pants", "Football Helmet", "Baseball Cap", "Golf Polo Shirt", 
             "Cycling Shorts", "Swimming Goggles", "Yoga Mat", "Wrestling Singlet", "Boxing Gloves", "Ski Jacket", "Snowboard Pants"]  
    return {
 
        'product_name': random.choice(style),
        'product_description': random.choice(items) ,
        'brand': random.choice(brands),
        'size_item': random.choice(size),
        'price': round(random.uniform(9.99, 999.99), 2),
        'stock_quantity': random.randint(0, 1000),
    }

def generate_order_data(user_ids, product_ids):
    """Generate fake order data with relationships"""
    if not user_ids or not product_ids:
        raise ValueError("user_ids and product_ids must not be empty")
    
    selected_product_id = random.choice(product_ids)
    quantity = random.randint(1, 5)
    total_amount = round(random.uniform(10.00, 500.00), 2)
    
    return {
        'customer_id': random.choice(user_ids),
        'product_id': selected_product_id,
        'quantity': quantity,
        'total_amount': total_amount,
        'order_status': random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
        'order_date': fake.date_time_between(start_date='-6m', end_date='now'),
        'shipping_address': fake.address().replace('\n', ', '),
        'employee_name': f'{fake.first_name()} {fake.last_name()}'
    }

def insert_fake_orders(count=30, batch_size=25):
    """Insert fake orders with proper relationships"""
    print(f"Generating {count} fake orders...")
    
    user_ids = get_existing_ids('customers', 'customer_id')
    product_ids = get_existing_ids('product', 'product_id')
    
    if not user_ids:
        print("No users found. Please insert users first.")
        return None
    
    if not product_ids:
        print("No products found. Please insert products first.")
        return None
    
    print(f"Found {len(user_ids)} users and {len(product_ids)} products")
    
    if count <= batch_size:

        orders = [generate_order_data(user_ids, product_ids) for _ in range(count)]
        return insert_batch_records('sales_transaction', orders)
    else:

        for i in range(0, count, batch_size):
            batch_count = min(batch_size, count - i)
            orders = [generate_order_data(user_ids, product_ids) for _ in range(batch_count)]
            insert_batch_records('sales_transaction', orders)
            print(f"Inserted batch {i//batch_size + 1}")

def generate_related_data_in_memory(num_users=50, num_products=50, num_orders=100):
    """Generate all related data in memory before inserting"""
    print("Generating related data in memory...")
    
    # Clear existing data first
    clear_tables()
    
    # Generate users - without customer_id
    users = []
    for i in range(num_users):
        user_data = generate_user_data()
        users.append(user_data)
    
    # Generate products - without product_id
    products = []
    for i in range(num_products):
        product_data = generate_product_data()
        products.append(product_data)
    
    # Insert users and products first
    print("Inserting users...")
    insert_batch_records('customers', users)
    
    print("Inserting products...")
    insert_batch_records('product', products)
    
    # Now get the actual IDs that were inserted by the database
    print("Fetching actual user and product IDs...")
    user_ids = get_existing_ids('customers', 'customer_id')
    product_ids = get_existing_ids('product', 'product_id')
    
    if not user_ids:
        print("Error: No user IDs found after insertion")
        return
    
    if not product_ids:
        print("Error: No product IDs found after insertion")
        return
    
    print(f"Found {len(user_ids)} users and {len(product_ids)} products")
    
    # Generate orders using the actual IDs from the database
    print("Generating orders with actual foreign key IDs...")
    orders = []
    for i in range(num_orders):
        order_data = generate_order_data(user_ids, product_ids)
        orders.append(order_data)
    
    print("Inserting orders...")
    insert_batch_records('sales_transaction', orders)
    
    print("All related data inserted successfully!")

# Main execution
if __name__ == "__main__":
    print("Starting fake data insertion...")
    
    # Generate all data with proper foreign key handling
    generate_related_data_in_memory(num_users=50, num_products=50, num_orders=100)
    
    print("Fake data insertion completed!")

