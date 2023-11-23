import os
import glob

from plutonkit.config import REQUIREMENT
from plutonkit.config.framework import STANDARD_LIBRARY

def generate_project_folder_cwd(reference_value):
    DIRECTORY = os.getcwd()
    os.makedirs(os.path.join(DIRECTORY, reference_value['details']['project_name']))

def generate_default_file(reference_value,name,content):
    DIRECTORY = os.getcwd()
    f = open(os.path.join(DIRECTORY, reference_value['details']['project_name'],name), 'w')
    f.write(content)
    f.close()

def generate_filesystem(reference_value):
    DIRECTORY = os.getcwd()
    framework_value = [val['name'] for key,val in enumerate(reference_value['command']) if val['type'] =='framework' ][0]
    framework_value_clean = framework_value.replace("package_", "")
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("core/management", "template/"+framework_value_clean)
    callback_template_filesystem(dir_path, os.path.join(DIRECTORY, reference_value['details']['project_name']))

def callback_template_filesystem(from_content, to_content):
    if os.path.exists(from_content):
        for name in glob.glob(os.path.join(from_content,"*")):
            is_file = os.path.isfile(name)
            is_dir = os.path.isdir(name)
            if is_file:
                print("::G")
                base_name = os.path.splitext(os.path.basename(name))
                ref_filename = name
                if len(base_name) >1 :
                    if base_name[1] ==".tpl":
                        ref_filename = os.path.join(to_content,base_name[0]+".py")
                    else:
                        ref_filename = os.path.join(to_content,os.path.basename(name))

                with open(name, 'r') as fi:
                    f_write = open(ref_filename, 'w')
                    f_write.write(fi.read())
                    f_write.close()

            if is_dir:
                print(name,":dir")

def generate_requirement(reference_value,library):
    DIRECTORY = os.getcwd()
    f = open(os.path.join(DIRECTORY, reference_value['details']['project_name'],REQUIREMENT), 'w')
    f.write('\n'.join(STANDARD_LIBRARY+library))
    f.close()
