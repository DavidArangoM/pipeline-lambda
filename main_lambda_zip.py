from classes.function_class import FunctionClass
from functions import lambda_zip_functions
from functions import lambda_trigger_functions

def main(configuration_instance):
    #lambda_zip_functions.check_if_lambda_is_being_updated(configuration_instance)
    #flag = lambda_zip_functions.check_if_lambda_exists(configuration_instance)
    flag=True
    if flag:
        print('[itau-info] - lambda does exist')
        # lambda_zip_functions.update_lambda_configuration(configuration_instance)
        # lambda_zip_functions.update_lambda_code(configuration_instance)
        lambda_zip_functions.create_trigger_configuration(configuration_instance)
    else:
        print('[itau-info] - lambda does not exist')
        lambda_zip_functions.create_lambda(configuration_instance)


