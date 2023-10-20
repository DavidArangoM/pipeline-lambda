#Libraries to install
# pip install GitPython
# git in the docker image
# pip3 install pyyaml
# pip3 install boto3

from functions import repository_functions
from functions import yaml_functions
from functions import util_functions
from functions import docker_functions
import main_lambda_zip


# Clone repository to get all necessary configuration
# Variables that have to be sent or caught from the execution
repo_name='company-lambda'
branch_tag='main'
repository_functions.clone(repo_name, branch_tag)
docker_functions.build_docker(repo_name)
docker_functions.run_docker(repo_name)


# Read specfic environment configuration
file_name='resources.yaml'
environment='development'
env_configuration = yaml_functions.read_env_configuration(file_name, environment)
function_instance = util_functions.map_function_configuration_to_class(env_configuration)
trigger_in_instance = util_functions.map_trigger_in_configuration_to_class(env_configuration)
trigger_out_instance = util_functions.map_trigger_out_configuration_to_class(env_configuration)
configuration_instance = util_functions.map_all_configuration_to_class(function_instance, trigger_in_instance, trigger_out_instance)
#fields = vars(trigger_in_instance)
#print(f'[itau-info] - environment configuration: {fields}')

if function_instance.code["zip"]["enable"] == True:
    print('[itau-info] - running lambda zip deployment')
    main_lambda_zip.main(configuration_instance)


if function_instance.code["docker"]["enable"] == True:
    print('[itau-info] - running lambda docker deployment')

print("END PROGRAM")