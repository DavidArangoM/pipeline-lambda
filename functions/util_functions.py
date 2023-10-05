import boto3
from classes.function_class import FunctionClass
from classes.trigger_in_class import TriggerInClass
from classes.trigger_out_class import TriggerOutClass
from classes.configuration_class import ConfigurationClass

#Description: Map yaml fields to function python class.
def map_function_configuration_to_class(env_configuration):
    root_field = "function"
    instance = FunctionClass(env_configuration[root_field]["accountId"],
                                      env_configuration[root_field]["region"],
                                      env_configuration[root_field]["name"],
                                      env_configuration[root_field]["description"],
                                      env_configuration[root_field]["role"],
                                      env_configuration[root_field]["timout"],
                                      env_configuration[root_field]["memory-size"],
                                      env_configuration[root_field]["storage-size"],                                      
                                      env_configuration[root_field]["vpc"],
                                      env_configuration[root_field]["runtime"],
                                      env_configuration[root_field]["layers"],
                                      env_configuration[root_field]["variables"],
                                      env_configuration[root_field]["code"])
    return instance

#Description: Map yaml fields to trigger in python class.
def map_trigger_in_configuration_to_class(env_configuration):
    root_field = "trigger_in"
    child_field = "triggers"
    triggers = env_configuration[root_field][child_field],
    instance = TriggerInClass(triggers)
    return instance 

#Description: Map yaml fields to trigger out python class.
def map_trigger_out_configuration_to_class(env_configuration):
    root_field = "trigger_in"
    instance = TriggerOutClass()
    return instance

#Description: Map yaml fields to configuration python class.
def map_all_configuration_to_class( function_instance, trigger_in_instance, trigger_out_instance):
    instance = ConfigurationClass(function_instance, trigger_in_instance, trigger_out_instance)
    return instance

#Description: Return boto3 lambda client to avoid boilerplate code.
def get_boto3_lambda_client(region):
    lambda_client = boto3.client('lambda', region_name=region)
    return lambda_client

#Description: Return boto3 s3 client to avoid boilerplate code.
def get_boto3_s3_client(region):
    s3_client = boto3.client('s3', region_name=region)
    return s3_client
