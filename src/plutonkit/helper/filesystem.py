"""Module providing a function printing python version."""

import os
import glob
from plutonkit.config import REQUIREMENT
from plutonkit.config.framework import STANDARD_LIBRARY
import yaml

def default_project_name(name):
    return f"{name}_project"

def generate_project_folder_cwd(project_name):
    directory = os.getcwd()
    os.makedirs(os.path.join(directory, default_project_name(project_name)))

def generate_requirement(project_name,library=[]):
    directory = os.getcwd()
    with open(os.path.join(directory, default_project_name(project_name),REQUIREMENT), "w", encoding="utf-8") as fw:
        fw.write("\n".join(STANDARD_LIBRARY+library+[""]))
        fw.close()

def create_yaml_file(project_name,filename,library={}):
    directory = os.getcwd()
    with open(os.path.join(directory, default_project_name(project_name),filename), "w", encoding="utf-8") as fw:
        fw.write(yaml.dump(library, default_flow_style=False))
        fw.close()

def write_file_content(directory,folder_name,file,content):
    file_path = os.path.dirname(file)
    if file_path != "":
        new_folder = os.path.join(directory, default_project_name(folder_name),file_path)
        if os.path.exists(new_folder) == False:
            os.makedirs(new_folder)

    name = os.path.join(directory, default_project_name(folder_name),file)
    base_name = os.path.splitext(name)
    if len(base_name) >1 :
        if base_name[1] == ".tpl":
            raw_filename = base_name[0]
            name = os.path.join(directory, default_project_name(folder_name),f"{raw_filename}.py")

    with open(name, "w") as f_write:
        f_write.write(  content )
        f_write.close()
