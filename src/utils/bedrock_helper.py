import json


def generate_sql(bedrock_client, natural_language_query, schema_info):
    """Generates SQL query from natural language input using Amazon Bedrock with schema context."""
    prompt = f"""
    You are an expert in SQL query generation. Given the following database schema:

    {schema_info}

    Convert the user's request into a valid SQL query:
    Request: {natural_language_query}
    """

    response = bedrock_client.invoke_model(
        modelId="amazon.claude-v2", body=json.dumps({"inputText": prompt})
    )

    return response["body"].read().decode("utf-8")
