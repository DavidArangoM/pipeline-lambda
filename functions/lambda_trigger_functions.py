import boto3
import time
from classes.function_class import FunctionClass
from functions import util_functions

def s3_trigger_add_permissions(configuration_instance):
    print('[itau-info] - adding lambda trigger permissions')
    
    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)
    response = lambda_client.add_permission(
        FunctionName=configuration_instance.function_instance.name,
        StatementId=configuration_instance.trigger_in_instance.policy["statementId"],
        Action=configuration_instance.trigger_in_instance.policy["action"],
        Principal=configuration_instance.trigger_in_instance.policy["principal"],
        SourceArn=configuration_instance.trigger_in_instance.policy["sourceArn"],
        SourceAccount=configuration_instance.trigger_in_instance.policy["accountId"]
    )

    httpStatusCode = response['ResponseMetadata']['HTTPStatusCode']
    if httpStatusCode != 204 and httpStatusCode != 201:
        print('[itau-error] - lambda trigger permissions could not be added: '+str(response))
        exit()

    print('[itau-info] - lambda trigger permissions added')

def s3_trigger_remove_permissions(configuration_instance):
    print('[itau-info] - removing lambda trigger permissions')
    
    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)
    response = lambda_client.remove_permission(
        FunctionName=configuration_instance.function_instance.name,
        StatementId=configuration_instance.trigger_in_instance.policy["statementId"]
    )

    httpStatusCode = response['ResponseMetadata']['HTTPStatusCode']
    if httpStatusCode != 204 and httpStatusCode != 201:
        print('[itau-error] - lambda trigger permissions could not be removed: '+str(response))
        exit()

    print('[itau-info] - lambda trigger permissions removed')

def check_event_source_mapping(configuration_instance):
    print('[itau-info] - checking current trigger configuration')

    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)
    response = lambda_client.list_event_source_mappings(
        FunctionName=configuration_instance.function_instance.name
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('[itau-error] - lambda trigger configuration could not be gotten: '+str(response))
        exit()

    print('[itau-info] - lambda trigger configuration gotten')
    print('[itau-info] - '+str(response))
