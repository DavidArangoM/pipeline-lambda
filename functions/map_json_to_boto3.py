import boto3

# Initialize the AWS Lambda client
lambda_client = boto3.client('lambda')

# Define your JSON object with the desired event source mapping configuration
event_source_mapping_config = {"FunctionName": "itau-lambda-dev", "EventSourceArn": "arn:aws:s3:::itau-bucket", "Enabled": True, "BatchSize": 10, "EventSource": "aws:s3"}

try:
    # Create the event source mapping using the JSON configuration
    response = lambda_client.create_event_source_mapping(**event_source_mapping_config)

    # Print the response or perform any other desired actions
    print(f"Event source mapping created: {response['UUID']}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
