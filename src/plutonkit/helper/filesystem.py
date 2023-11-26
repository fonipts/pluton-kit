"""Module providing a function printing python version."""

import os
import glob

from plutonkit.config import REQUIREMENT
from plutonkit.config.framework import STANDARD_LIBRARY

def default_project_name(name):
    return f'{name}_project'

def generate_project_folder_cwd(reference_value):
    directory = os.getcwd()
    os.makedirs(os.path.join(directory, default_project_name(reference_value['details']['project_name'])))

def generate_default_file(reference_value,name,content):
    directory = os.getcwd()
    with open(os.path.join(directory, default_project_name(reference_value['details']['project_name']),name), 'w', encoding="utf-8") as fw:
        fw.write(content)
        fw.close()

def generate_filesystem(reference_value,sub_folder=None):
    directory = os.getcwd()
    framework_value = [val['name'] for key,val in enumerate(reference_value['command']) if val['type'] =='framework' ][0]
    framework_value_clean = framework_value.replace("package_", "")
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("helper", f"template/{framework_value_clean}")
    if sub_folder is None:
        callback_template_filesystem(dir_path, os.path.join(directory, default_project_name(reference_value['details']['project_name'])),{})
    else:
        callback_template_filesystem(dir_path, os.path.join(directory, default_project_name(reference_value['details']['project_name']),sub_folder),{})

def callback_template_filesystem(from_content, to_content,variable):

    if os.path.exists(from_content):
        for name in glob.glob(os.path.join(from_content,"*")):
            is_file = os.path.isfile(name)
            is_dir = os.path.isdir(name)
            if is_file:

                base_name = os.path.splitext(os.path.basename(name))
                ref_filename = name
                if len(base_name) >1 :
                    if base_name[1] ==".tpl":
                        ref_filename = os.path.join(to_content,f"{base_name[0]}.py")
                    else:
                        ref_filename = os.path.join(to_content,os.path.basename(name))

                with open(name, 'r', encoding="utf-8") as fi:
                    with open(ref_filename, 'w') as f_write:
                        f_write.write(fi.read())
                        f_write.close()

            if is_dir:
                new_path = name.replace(from_content, "").replace("/", "")
                new_dir = os.path.join(to_content,new_path)
                os.makedirs(new_dir)
                callback_template_filesystem(os.path.join(from_content,new_path), new_dir ,variable)

def generate_requirement(reference_value,library):
    directory = os.getcwd()
    with open(os.path.join(directory, default_project_name(reference_value['details']['project_name']),REQUIREMENT), 'w', encoding="utf-8") as fw:
        fw.write('\n'.join(STANDARD_LIBRARY+library))
        fw.close()
