import json
from classes.function_class import FunctionClass
from functions import util_functions
from functions import lambda_zip_functions

def s3_put_bucket_notification_configuration(configuration_instance, trigger):
    print('[itau-info] - putting s3 notification')

    s3_client = util_functions.get_boto3_s3_client(configuration_instance.function_instance.region)
    lambda_arn = lambda_zip_functions.build_lambda_arn(configuration_instance)

    notification_configuration  = {
    'LambdaFunctionConfigurations': [{
        'LambdaFunctionArn': lambda_arn,
        'Events': trigger['events'],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'prefix',
                            'Value':  trigger['filters']['prefix']
                        },
                        {
                            'Name': 'suffix',
                            'Value':  trigger['filters']['suffix']
                        }
                    ]
                }
            }
        },
    ],}
    
    response = s3_client.put_bucket_notification_configuration(
        Bucket=trigger['bucketName'],
        NotificationConfiguration=notification_configuration
    )
    
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('[itau-error] - event could not be putted: '+str(response))
        exit()

    print('[itau-info] - event putted')