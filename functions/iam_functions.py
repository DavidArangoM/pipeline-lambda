import json
from functions import util_functions
from config import config

def create_role(configuration_instance):
    print('[itau-info] - creating iam role')

    iam_client = util_functions.get_boto3_iam_client(configuration_instance.function_instance.region)

    if not check_if_role_exists(configuration_instance):    
        response = iam_client.create_role(
            RoleName=configuration_instance.function_instance.role['name'],
            AssumeRolePolicyDocument=json.dumps(config.lambda_assume_role_policy),
            Description='Role to be used in lambda functions',
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 200 and response['ResponseMetadata']['HTTPStatusCode'] != 201:
            print('[itau-error] - lambda role could not be created: '+str(response))
            exit()

        print('[itau-info] - lambda role created')
    else:
        print('[itau-info] - reusing lambda role - please check the permissions for that role')

def attach_policy_to_role(configuration_instance):
    print('[itau-info] - attaching policy to role')

    iam_client = util_functions.get_boto3_iam_client(configuration_instance.function_instance.region)

    response = iam_client.put_role_policy(
        RoleName=configuration_instance.function_instance.role['name'],
        PolicyName=configuration_instance.function_instance.role['customPolicyName'],
        PolicyDocument=json.dumps(config.lambda_role_custom_policy)
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200 and response['ResponseMetadata']['HTTPStatusCode'] != 201:
        print('[itau-error] - policy could not be atatched to role: '+str(response))
        exit()
    else:
        print('[itau-info] - policy attached to role')

def check_if_role_exists(configuration_instance):
    print('[itau-info] - checking if lambda role exists')

    iam_client = util_functions.get_boto3_iam_client(configuration_instance.function_instance.region)
    
    try: 
        response = iam_client.get_role(
            RoleName= configuration_instance.function_instance.role['name']
        )
        print('[itau-info] - lambda role exist')
        return True
    except iam_client.exceptions.NoSuchEntityException:
        print('[itau-info] - lambda role does not exist')
        return False

def build_iam_arn(accountId, iam_resource, type):
    arn = 'arn:aws:iam::' + accountId  + ':' + type +'/' + iam_resource    
    return arn

# def create_policy(configuration_instance):
#     print('[itau-info] - creating lambda role policy')

#     iam_client = util_functions.get_boto3_iam_client(configuration_instance.function_instance.region)

#     if not check_if_policy_exists(configuration_instance):    
#         response = iam_client.create_policy(
#             PolicyName=configuration_instance.role_instance.customPolicyName,
#             PolicyDocument=json.dumps(config.lambda_role_custom_policy),
#             Description='Custom policy for lambda role',
#         )

#         if response['ResponseMetadata']['HTTPStatusCode'] != 200 and response['ResponseMetadata']['HTTPStatusCode'] != 201:
#             print('[itau-error] - lambda role policy could not be created: '+str(response))
#             exit()
#     else:
#         print('[itau-info] - reusing lambda role policy - please check the permissions for that policy')

# def check_if_policy_exists(configuration_instance):
#     print('[itau-info] - checking if lambda role policy exists')

#     iam_client = util_functions.get_boto3_iam_client(configuration_instance.function_instance.region)

#     custom_policy_arn = build_iam_arn(configuration_instance)
    
#     try: 
#         response = iam_client.get_policy(
#             PolicyArn=custom_policy_arn
#         )
#         print('[itau-info] - lambda role policy exist')
#         return True
#     except iam_client.exceptions.NoSuchEntityException:
#         print('[itau-info] - lambda role policy does not exist')
#         return False
    
