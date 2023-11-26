"""Module providing a function printing python version."""
import os
import subprocess

from plutonkit.config import REQUIREMENT
from plutonkit.helper.filesystem import default_project_name

def pip_install_requirement(reference_value):
    directory = os.getcwd()
    path = os.path.join(directory, default_project_name(reference_value['details']['project_name']),REQUIREMENT)
    subprocess.call(['pip','install','-r',path])

def change_dir_command(reference_value):
    directory = os.getcwd()
    path = os.path.join(directory, default_project_name(reference_value['details']['project_name']))
    os.chdir(path)

def pip_run_command(command):

    subprocess.call(command)
