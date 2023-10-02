import boto3

# Initialize the AWS Lambda client
lambda_client = boto3.client('lambda')

# Define your JSON object with the desired event source mapping configuration
event_source_mapping_config = {
    "FunctionName": "your-lambda-function-name",
    "EventSourceArn": "your-event-source-arn",
    "Enabled": True,  # Set to True to enable the event source mapping
    "BatchSize": 10,  # Set your desired batch size
    "StartingPosition": "TRIM_HORIZON"  # Set your desired starting position
}

try:
    # Create the event source mapping using the JSON configuration
    response = lambda_client.create_event_source_mapping(**event_source_mapping_config)

    # Print the response or perform any other desired actions
    print(f"Event source mapping created: {response['UUID']}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
