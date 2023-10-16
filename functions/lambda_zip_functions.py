import boto3
from botocore.exceptions import ClientError
import time
import json
from classes.function_class import FunctionClass
from functions import util_functions
from functions import lambda_trigger_functions
from functions import iam_functions
from config import config

#Description: Take the configuration from the yaml file and create aws lambda.
def create_lambda(configuration_instance):
    print('[itau-info] - creating lambda')

    # Read the ZIP file as binary data
    zip_file_path = f'./{configuration_instance.function_instance.name}.zip'
    code_zip = ''
    with open(zip_file_path, 'rb') as zip_file:
        code_zip = zip_file.read()

    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)
    response = lambda_client.create_function(
        FunctionName=configuration_instance.function_instance.name,
        Description=configuration_instance.function_instance.description,
        Runtime=configuration_instance.function_instance.runtime['runtime'],
        Handler=configuration_instance.function_instance.runtime['handler'],
        Role= iam_functions.build_iam_arn(configuration_instance.function_instance.accountId, configuration_instance.function_instance.role['name'], 'role'),      
        Timeout=configuration_instance.function_instance.timeout,
        MemorySize= configuration_instance.function_instance.memory_size,
        PackageType='Zip',
        Publish=True,
        Architectures=configuration_instance.function_instance.runtime['architecture'],
        EphemeralStorage={
            'Size': configuration_instance.function_instance.storage_size
        },
        VpcConfig={
            'SubnetIds': configuration_instance.function_instance.vpc["subnets"],
            'SecurityGroupIds': configuration_instance.function_instance.vpc["security-groups"]
        },
        Environment={
            'Variables': configuration_instance.function_instance.variables
        },        
        Layers= configuration_instance.function_instance.layers,
        SnapStart={
            'ApplyOn': 'None'
        },
        Code={
            'ZipFile': code_zip
        }        
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200 and response['ResponseMetadata']['HTTPStatusCode'] != 201:
        print('[itau-error] - lambda could not be created: '+str(response))
        exit()

    print('[itau-info] - lambda created')

#Description: Take the configuration from the yaml file and update aws lambda.
def update_lambda_configuration(configuration_instance):
    print('[itau-info] - updating lambda configuration')
    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)
    response = lambda_client.update_function_configuration(
        FunctionName=configuration_instance.function_instance.name,
        Description=configuration_instance.function_instance.description,
        Role=iam_functions.build_iam_arn(configuration_instance.function_instance.accountId, configuration_instance.function_instance.role['name'], 'role'),
        Handler=configuration_instance.function_instance.runtime['handler'],
        Runtime=configuration_instance.function_instance.runtime['runtime'],        
        Timeout=configuration_instance.function_instance.timeout,
        MemorySize= configuration_instance.function_instance.memory_size,
        EphemeralStorage={
            'Size': configuration_instance.function_instance.storage_size
        },
        VpcConfig={
            'SubnetIds': configuration_instance.function_instance.vpc["subnets"],
            'SecurityGroupIds': configuration_instance.function_instance.vpc["security-groups"]
        },
        Environment={
            'Variables': configuration_instance.function_instance.variables
        },        
        Layers= configuration_instance.function_instance.layers
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('[itau-error] - lambda configuration could not be updated: '+str(response))
        exit()

    print('[itau-info] - lambda configuration updated')    

#Description: Take the zip code and push it to aws lammbda.
def update_lambda_code(configuration_instance):
    print('[itau-info] - updating lambda code')
    check_if_lambda_is_being_updated(configuration_instance)

    # Read the ZIP file as binary data
    zip_file_path = f'./{configuration_instance.function_instance.name}.zip'
    code_zip = ''
    with open(zip_file_path, 'rb') as zip_file:
        code_zip = zip_file.read()
    
    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)
    response = lambda_client.update_function_code(
        FunctionName=configuration_instance.function_instance.name,
        ZipFile=code_zip,
        Publish=True,
        Architectures=configuration_instance.function_instance.runtime['architecture']
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('[itau-error] - lambda code could not be updated: '+str(response))
        exit()

    print('[itau-info] - lambda code updated')

#Description: List all lambda functions and check if one of them match.
def check_if_lambda_exists(configuration_instance):
    print(f'[itau-info] - checking if "{configuration_instance.function_instance.name}" exists on "{configuration_instance.function_instance.region}"')
    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)
    response = lambda_client.list_functions()

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('[itau-error] - the lambda existence could not be validated: '+str(response))
        exit()
    
    functions = response["Functions"]
    #print('[itau-info] - lambda list retrieved: '+str(functions))
    for function in functions:
        if function['FunctionName'] == configuration_instance.function_instance.name:
            return True
    return False

#Description: Check if the lambda is being updated to wait for it.
def check_if_lambda_is_being_updated(configuration_instance):
    print(f'[itau-info] - checking if "{configuration_instance.function_instance.name}" is being updated')
    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)
    try:
        response = lambda_client.get_function(FunctionName=configuration_instance.function_instance.name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("[itau-info] - lambda does not exists")
            return

    if response['Configuration']['LastUpdateStatus'] == 'InProgress':
        print("[itau-info] - the Lambda function has an update in progress, waiting 15 seconds.")
        time.sleep(15)
        check_if_lambda_is_being_updated(configuration_instance)

#Description: Check there is a policy for the function.
def check_if_function_policy_exists(configuration_instance, statementId):
    print('[itau-info] - checking if function policy exists for trigger')

    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)
    try:
        response = lambda_client.get_policy(FunctionName=configuration_instance.function_instance.name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("[itau-info] - Policy not found")
            return False

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('[itau-error] - lambda policy existence could not be gotten: '+str(response))
        exit()
    
    policy = json.loads(response['Policy'])
    # print(policy['Statement'])
    statement_list = policy['Statement']
    for statement in  statement_list:
        #cambiar acá
        if statementId == str(statement['Sid']):
            print("[itau-info] - Policy for trigger found")
            return True
    
    print("[itau-info] - Policy for trigger not found")
    return False

#Description: Create all necessary in-trigger configuration
def create_trigger_in_configuration(configuration_instance):
    print('[itau-info] - creating/updating lambda in-trigger')

    #get all triggers_in
    triggers = configuration_instance.trigger_in_instance.triggers[0]

    #Validate if there is a existing policy
    for trigger in triggers:
        trigger_in_policy =  triggers[trigger]['policy']
        flag = check_if_function_policy_exists(configuration_instance, trigger_in_policy['statementId'])
        if flag:
           lambda_trigger_functions.lambda_trigger_remove_permissions(configuration_instance, trigger_in_policy)
        lambda_trigger_functions.lambda_trigger_add_permissions(configuration_instance, trigger_in_policy)
        #lambda_trigger_functions.lambda_trigger_check_event_source_mapping(configuration_instance)   
        lambda_trigger_functions.lambda_trigger_add_event_source_mapping(configuration_instance, triggers[trigger]) 
    
    
    print('[itau-info] - lambda in-trigger created/updated')

#Description: Create all necessary out-trigger configuration
def create_trigger_out_configuration(configuration_instance):
    print('[itau-info] - creating/updating lambda out-trigger')

    #get all triggers_out
    triggers = configuration_instance.trigger_out_instance.triggers[0]

    #get lambda client
    lambda_client = util_functions.get_boto3_lambda_client(configuration_instance.function_instance.region)

    #Validate if there is a existing policy
    for trigger in triggers:
        on_success = triggers[trigger]["onSuccess"]
        on_failure = triggers[trigger]["onFailure"]
        if len(on_success) == 0 or len(on_failure) == 0:
            print('[itau-error] - onSuccess and onFailure can not be empty')
            exit()
        
        trigger_out_types = config.configuration["trigger_out_types"]
        
        if not util_functions.is_a_valid_arn(on_success, trigger_out_types):
            print(f'[itau-error] - onSuccess arn is related to a service dont allowed')
            exit()
        
        if not util_functions.is_a_valid_arn(on_failure, trigger_out_types):
            print(f'[itau-error] - onFailure arn is related to a service dont allowed')
            exit()
        
        response = lambda_client.put_function_event_invoke_config(
            FunctionName=configuration_instance.function_instance.name,
            MaximumRetryAttempts= triggers[trigger]["MaximumRetryAttempts"],
            DestinationConfig={
                'OnSuccess': {
                    'Destination': on_success
                },
                'OnFailure': {
                    'Destination': on_failure
                }
            }
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            print('[itau-error] - lambda code could not be updated: '+str(response))
            exit()
    
    print('[itau-info] - lambda out-trigger created/updated')

#Description: Build Lambda arn
def build_lambda_arn(configuration_instance):
    arn = 'arn:aws:lambda:' + configuration_instance.function_instance.region + ':' + configuration_instance.function_instance.accountId + ':function:' + configuration_instance.function_instance.name
    return arn