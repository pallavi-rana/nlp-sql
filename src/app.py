import streamlit as st
import boto3
from utils.s3_helper import upload_files
from utils.bedrock_helper import generate_sql
from utils.athena_helper import (get_aws_schema,
                                 execute_athena_query,
                                 get_athena_results)

# Set tab title and favicon
st.set_page_config(page_title="Natural Language to SQL Query Generator")

# AWS Configuration
AWS_REGION = "us-east-1"
S3_BUCKET = "pallavi-data-bucket"
ATHENA_DATABASE = "nlp_database"
S3_OUTPUT = f"s3://{S3_BUCKET}/athena-results/"

# Initialize AWS clients
athena_client = boto3.client("athena", region_name=AWS_REGION)
bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
glue_client = boto3.client("glue", region_name=AWS_REGION)

# Streamlit UI
st.title("NLP to SQL Query Generator")

# Data Refresh Button
if st.button("Refresh Data"):
    with st.spinner("Uploading CSV files and refreshing database..."):
        upload_files()
        glue_client.start_crawler(Name="csv-data-crawler")  # Run AWS Glue Crawler
    st.success("Data Refreshed Successfully!")

# User Input for NLP Query
natural_query = st.text_input("Enter your query in English:")

# Process NLP Query
if st.button("Generate SQL and Fetch Results"):
    if not natural_query.strip():
        st.warning("Please enter a query before submitting!")
    else:
        with st.spinner("Generating SQL query..."):
            schema_info = get_aws_schema(athena_client, ATHENA_DATABASE, S3_OUTPUT)
            sql_query = generate_sql(bedrock_client, natural_query, schema_info)
            st.write(f"Generated SQL Query:`{sql_query}`")

        with st.spinner("Executing SQL query in Athena..."):
            query_execution_id = execute_athena_query(
                athena_client, sql_query, ATHENA_DATABASE, S3_OUTPUT
            )
            results = get_athena_results(athena_client, query_execution_id)

        st.success("Query Execution Completed!")
        st.write("Query Results:", results)
