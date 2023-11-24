import subprocess
import os

from plutonkit.config import REQUIREMENT

def pip_install_requirement(reference_value):
    DIRECTORY = os.getcwd()
    path = os.path.join(DIRECTORY, reference_value['details']['project_name'],REQUIREMENT)
    subprocess.call(['pip','install','-r',path])

def change_dir_command(reference_value):
    DIRECTORY = os.getcwd()
    path = os.path.join(DIRECTORY, reference_value['details']['project_name'])
    os.chdir(path)

def pip_run_command(command):

    subprocess.call(command)

