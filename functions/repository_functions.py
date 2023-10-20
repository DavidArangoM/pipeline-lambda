from git import Repo
import os
import subprocess
import shutil

git_base_url='https://github.com/DavidArangoM/'

def clone(repo_name, branch_tag):
    repo_url = git_base_url + repo_name + '.git'
    #Print parameters
    print('[itau-info] - repository to clone: '+repo_url)
    print('[itau-info] - branch or tag to be checkout: '+branch_tag)

    if os.path.exists(repo_name):
        print(f'[itau-info] - folder/repository {repo_name} exists, removing it')
        try:
            shutil.rmtree(repo_name)
        except OSError as e:
           print('[itau-error] - folder could not be removed: '+str(e))

    try:
        #Clone repository in current directory
        subprocess.run(['git', 'clone', repo_url])
        print('[itau-info] - repository cloned!')
    except Exception as e:
        print('[itau-error] - repository could not be cloned: '+str(e))

    try:
        #Checkout to branch or tag
        original_directory = os.getcwd()
        os.chdir(repo_name)
        os.system('git checkout '+branch_tag)
        os.chdir(original_directory)
        print('[itau-info] - checkout done to specific branch or tag!')
    except Exception as e:
        print('[itau-error] - checkout could not be done: '+str(e))
    

    

