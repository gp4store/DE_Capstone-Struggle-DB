import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://user:password@host:port/database"
engine = create_engine(DATABASE_URL)

# Create DataFrame
df = pd.DataFrame({
    'name': ['John Doe', 'Alice Smith', 'Bob Johnson'],
    'email': ['john@example.com', 'alice@example.com', 'bob@example.com']
})

# Insert to database
df.to_sql('users', engine, if_exists='append', index=False, method='multi')