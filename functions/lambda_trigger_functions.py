import boto3
import time
import json
from classes.function_class import FunctionClass
from functions import util_functions
from functions import s3_functions

def lambda_trigger_add_permissions(configuration_instance, trigger_policy):
    print('[itau-info] - adding lambda trigger permissions')
    
    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)
    response = lambda_client.add_permission(
        FunctionName=configuration_instance.function_instance.name,
        StatementId=trigger_policy["statementId"],
        Action=trigger_policy["action"],
        Principal=trigger_policy["principal"],
        SourceArn=trigger_policy["sourceArn"],
        SourceAccount=trigger_policy["accountId"]
    )

    httpStatusCode = response['ResponseMetadata']['HTTPStatusCode']
    if httpStatusCode != 204 and httpStatusCode != 201:
        print('[itau-error] - lambda trigger permissions could not be added: '+str(response))
        exit()

    print('[itau-info] - lambda trigger permissions added')

def lambda_trigger_remove_permissions(configuration_instance, trigger_policy):
    print('[itau-info] - removing lambda trigger permissions')
    
    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)
    response = lambda_client.remove_permission(
        FunctionName=configuration_instance.function_instance.name,
        StatementId=trigger_policy["statementId"]
    )

    httpStatusCode = response['ResponseMetadata']['HTTPStatusCode']
    if httpStatusCode != 204 and httpStatusCode != 201:
        print('[itau-error] - lambda trigger permissions could not be removed: '+str(response))
        exit()

    print('[itau-info] - lambda trigger permissions removed')

def lambda_trigger_check_event_source_mapping(configuration_instance):
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

def lambda_trigger_add_event_source_mapping(configuration_instance, trigger):
    print('[itau-info] - adding event source mapping for '+str(trigger['type']))
  
    if trigger['type'] == 's3':
        print('[itau-info] - adding s3 trigger')
        s3_functions.s3_put_bucket_notification_configuration(configuration_instance, trigger)
    else:
        print('[itau-info] - adding other trigger')
        #response = lambda_client.create_event_source_mapping(**triggers[trigger])
        #  if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        #     print('[itau-error] - event source mapping could not be added: '+str(response))
        #     exit()

    print('[itau-info] - event source mapping added')