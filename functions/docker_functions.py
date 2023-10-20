import subprocess
import os
def build_docker(repo_name):
    print('[itau-info] - building repository docker image')
    original_directory = os.getcwd()
    os.chdir(repo_name)
    try:
        subprocess.run(["docker", "build", "-t", repo_name, "."], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print('[itau-error] - docker could not be built: '+str(e))
    os.chdir(original_directory)

def run_docker(repo_name):
    print('[itau-info] - running docker container to generate the zip file')
    original_directory = os.getcwd()
    os.chdir(repo_name)
    try:
        subprocess.run(["docker", "run", "--rm", "-v", original_directory + "/deploy:/deploy", repo_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print('[itau-error] - docker could not be run: '+str(e))
    os.chdir(original_directory)