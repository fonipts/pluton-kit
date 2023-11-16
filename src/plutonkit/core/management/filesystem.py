import os
from plutonkit.config import REQUIREMENT

def generate_project_folder_cwd(reference_value):
    DIRECTORY = os.getcwd()
    os.makedirs(os.path.join(DIRECTORY, reference_value['details']['project_name']))

def generate_default_file(reference_value,name,content):
    DIRECTORY = os.getcwd()
    f = open(os.path.join(DIRECTORY, reference_value['details']['project_name'],name), 'w')
    f.write(content)
    f.close()
    #os.makedirs(os.path.join(DIRECTORY, reference_value['details']['project_name']))

def generate_requirement(reference_value,library):
    DIRECTORY = os.getcwd()
    f = open(os.path.join(DIRECTORY, reference_value['details']['project_name'],REQUIREMENT), 'w')
    f.write('\n'.join(library))
    f.close()
