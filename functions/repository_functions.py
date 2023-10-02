from git import Repo
import os

git_base_url='https://github.com/DavidArangoM/'

def clone(repo_name, branch_tag):
    repo_url = git_base_url + repo_name + '.git'
    #Print parameters
    print('[itau-info] - repository to clone: '+repo_url)
    print('[itau-info] - branch or tag to be checkout: '+branch_tag)

    try:
        #Clone repository in current directory
        os.system('git clone '+repo_url)
        print('[itau-info] - repository cloned!')
    except Exception as e:
        print('[itau-error] - repository could not be cloned')
        print(e)

    try:
        #Checkout to branch or tag
        os.chdir(repo_name)
        os.system('git checkout '+branch_tag)
        print('[itau-info] - checkout done to specific branch or tag!')
    except Exception as e:
        print('[itau-error] - checkout could not be done')
        print(e)
    

    

