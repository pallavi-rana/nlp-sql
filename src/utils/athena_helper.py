import time


def get_aws_schema(athena_client, database, s3_output):
    """Fetch schema details for tables in the AWS Glue Data Catalog."""
    query = f"SHOW TABLES IN {database};"
    query_execution_id = execute_athena_query(query, database, s3_output, athena_client)
    tables = get_athena_results(query_execution_id, athena_client)

    schema_info = ""
    for table in tables["ResultSet"]["Rows"][1:]:
        table_name = table["Data"][0]["VarCharValue"]
        describe_query = f"DESCRIBE {database}.{table_name};"
        query_execution_id = execute_athena_query(
            describe_query, database, s3_output, athena_client
        )
        columns = get_athena_results(query_execution_id, athena_client)

        schema_info += f"\nTable: {table_name}\n"
        for column in columns["ResultSet"]["Rows"][1:]:
            schema_info += f"{column['Data'][0]['VarCharValue']} ({column['Data'][1]['VarCharValue']})\n"

    return schema_info


def execute_athena_query(athena_client, sql_query, database, s3_output):
    """Executes SQL query on AWS Athena and waits for completion."""
    response = athena_client.start_query_execution(
        QueryString=sql_query,
        QueryExecutionContext={"Database": database},
        ResultConfiguration={"OutputLocation": s3_output},
    )

    query_execution_id = response["QueryExecutionId"]

    while True:
        status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        state = status["QueryExecution"]["Status"]["State"]
        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
        time.sleep(2)

    return query_execution_id


def get_athena_results(athena_client, query_execution_id):
    """Fetches query results from AWS Athena."""
    return athena_client.get_query_results(QueryExecutionId=query_execution_id)
