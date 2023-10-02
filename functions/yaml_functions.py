import yaml

#Read complete yaml file---
def read_yaml_file(file_name):
    data=''
    try:
        with open(file_name, 'r') as file:
            data = yaml.safe_load(file)
        print('[itau-info] - yaml file read!')
    except Exception as e:
        print('[itau-error] - yaml could not be read')
        print(e)
        exit()
    return data

#Read environment configuration in yaml file---
def read_env_configuration(file_name, environment):
    data = read_yaml_file(file_name)
    try:
        data = data[environment]
        print('[itau-info] - environment configuration gotten!')
    except Exception as e:
        print(f'[itau-error] - env configuration "{environment}" not found')
        print(e)
        exit()
    return data

#Read function properties in yaml file---
def read_function_configuration(file_name, environment, function_field):
    data = read_yaml_file(file_name)
    try:
        data = data[environment]["function"][function_field]
        print('[itau-info] - environment configuration gotten!')
    except Exception as e:
        print(f'[itau-error] - env configuration "{environment}" not found')
        print(e)
    print(data)
    return ''