# ETL Pipeline - Struggle Database

A serverless ETL pipeline built on AWS that processes sales data from the fictional "Struggle" database. This pipeline demonstrates data ingestion, transformation, and loading using AWS Glue, with automated schema discovery and scalable data processing.

## Overview

This project implements an end-to-end ETL pipeline that processes three main data sources:
- **Customers**: Customer demographic and contact information
- **Products**: Product catalog with pricing and category data  
- **Sales Transactions**: Order history and transaction details

The pipeline uses AWS Glue for serverless data processing and S3 for durable data storage, automatically discovering schemas and transforming raw CSV data into analytics-ready formats.

## Architecture

```
S3 (Raw Data) → Glue Crawlers → Glue Data Catalog → Glue Jobs → S3 (Processed Data)
```

### Components
- **AWS S3**: Source and destination data storage
- **AWS Glue Crawlers**: Automated schema discovery and cataloging
- **AWS Glue Jobs**: Data transformation and processing (PySpark)
- **AWS Glue Data Catalog**: Centralized metadata repository

## Repository Structure

```
├── data/
│   ├── raw/                    # Sample input CSV files
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   └── sales_transactions.csv
│   └── processed/              # Output data location
├── scripts/
│   ├── glue_jobs/             # Glue job Python scripts
│   ├── crawlers/              # Crawler configuration
│   └── data_generation/       # Faker scripts for test data
├── config/
│   └── pipeline_config.py     # Configuration settings
└── README.md
```

## Prerequisites

### AWS Resources
- AWS Account with appropriate permissions
- S3 buckets for raw and processed data
- IAM roles for Glue jobs and crawlers

### Required Permissions
- `AWSGlueServiceRole`
- S3 read/write access to data buckets
- CloudWatch Logs access for monitoring

## Setup

### 1. Environment Setup
```bash
pip install boto3 faker pandas
```

### 2. AWS Configuration
```bash
aws configure
# Set your AWS credentials and region
```

### 3. S3 Bucket Creation
Create S3 buckets for:
- Raw data storage: `s3://your-bucket-raw/`
- Processed data storage: `s3://your-bucket-processed/`

### 4. Deploy Glue Resources
- Upload Glue job scripts to S3
- Create Glue crawlers for source data
- Configure Glue jobs with appropriate parameters

## Usage

### Data Generation
Generate sample data using the Faker-based scripts:
```python
python scripts/data_generation/generate_struggle_data.py
```

### Running the Pipeline

1. **Upload raw data** to S3 raw bucket
2. **Run crawlers** to discover schemas:
   ```bash
   aws glue start-crawler --name customers-crawler
   aws glue start-crawler --name products-crawler
   aws glue start-crawler --name transactions-crawler
   ```
3. **Execute Glue jobs** for data transformation
4. **Processed data** will be available in the S3 processed bucket

### Sample Data Format

**Customers CSV:**
```csv
customer_id,first_name,last_name,email,phone,city,state
1,John,Doe,john.doe@email.com,555-0123,New York,NY
```

**Products CSV:**
```csv
product_id,product_name,category,price,description
1,Widget A,Electronics,29.99,High-quality widget
```

**Sales Transactions CSV:**
```csv
transaction_id,customer_id,product_id,quantity,transaction_date,total_amount
1,1,1,2,2024-01-15,59.98
```

## Monitoring & Logging

- **CloudWatch Logs**: All Glue jobs log to CloudWatch for debugging
- **Job Bookmarks**: Enabled to process only new data incrementally
- **Data Quality**: Built-in validation and error handling

## Key Features

- **Automated Schema Discovery**: Crawlers automatically detect data structures
- **Scalable Processing**: Serverless Glue jobs scale based on data volume
- **Cost Effective**: Pay-per-use model with automatic resource management
- **Data Cataloging**: Centralized metadata for analytics tools
- **Error Handling**: Comprehensive logging and error recovery

## Configuration

Key configuration parameters in `config/pipeline_config.py`:
- S3 bucket paths
- Glue job settings
- Data transformation rules
- Logging levels

## Performance Notes

- Typical processing time: 5-15 minutes for moderate datasets
- DPU allocation: Configurable based on data volume
- Partitioning: Output data partitioned by date for optimal query performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with sample data
5. Submit a pull request

## License

This project is for educational and demonstration purposes.

## Future Enhancements

- [ ] Add data quality checks and validation
- [ ] Implement incremental processing optimization
- [ ] Add integration with AWS QuickSight for visualization
- [ ] Implement automated testing framework
- [ ] Add support for real-time streaming data
