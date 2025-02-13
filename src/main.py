from utils.s3_helper import upload_files
from utils.bedrock_helper import generate_sql
from utils.athena_helper import get_aws_schema, execute_athena_query, get_athena_results
import boto3

# AWS Configuration
AWS_REGION = "us-east-1"
S3_BUCKET = "pallavi-data-bucket"
ATHENA_DATABASE = "nlp_database"
S3_OUTPUT = f"s3://{S3_BUCKET}/athena-results/"

# Initialize AWS clients
aws_region = "us-east-1"
s3_client = boto3.client("s3", region_name=aws_region)
athena_client = boto3.client("athena", region_name=aws_region)
bedrock_client = boto3.client("bedrock-runtime", region_name=aws_region)

# Automatically upload CSV files to S3
print("Uploading CSV files to S3...")
upload_files()

# Get user input (natural language query)
natural_query = input("Enter your query in natural language: ")

# Convert query to SQL using Amazon Bedrock
schema_info = get_aws_schema(athena_client, ATHENA_DATABASE, S3_OUTPUT)
sql_query = generate_sql(bedrock_client, natural_query, schema_info)
print(f"Generated SQL Query: {sql_query}")

# Execute the query in Athena
query_execution_id = execute_athena_query(
    athena_client, sql_query, ATHENA_DATABASE, S3_OUTPUT
)

# Fetch and display results
results = get_athena_results(
    athena_client,
    query_execution_id,
)
print(f"Query Results: {results}")
