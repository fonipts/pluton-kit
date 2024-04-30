"""Module providing a function printing python version."""

from yaml import  dump

from plutonkit.framework.package.django_script import DjangoScript
from plutonkit.config import ARCHITECTURE_DETAILS_FILE,PROJECT_COMMAND_FILE,PROJECT_DETAILS_FILE
import requests

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from plutonkit.helper.filesystem import create_yaml_file,default_project_name, generate_project_folder_cwd ,generate_requirement,write_file_content
import yaml

from plutonkit.helper.command import pip_install_requirement,pip_run_command

import os
import sys

class FrameworkBluePrint:
    def __init__(self,path) -> None:
        self.path = path
        self.folder_name = ""
        self.directory = os.getcwd()
    def set_folder_name(self, name):
        self.folder_name = name

    def execute(self):
        data = self._curl(f"{self.path}/{ARCHITECTURE_DETAILS_FILE}")
        if data.status_code == 200:

            try:
                generate_project_folder_cwd(self.folder_name)
                content = load(str(data.text), Loader=Loader)

                dependencies = content.get("dependencies",[])
                files = content.get("files",[])
                script = content.get("script",{})

                create_yaml_file(self.folder_name,PROJECT_DETAILS_FILE,{
                    "name": self.folder_name,
                    "blueprint": self.path
                })
                create_yaml_file(self.folder_name,PROJECT_COMMAND_FILE,{
                    "script": script
                })

                self._packages(dependencies)
                self._files(files)

            except Exception as e:
                print(e)
                print("Invalid yaml file content")
                sys.exit(0)
        else:
            print("Can not access, please try again later")

    def _curl(self,path):
        data = requests.get(path)
        return data

    def _packages(self,values):
        default_item = values.get("default",[])
        library = []
        for value in default_item:
            pip_run_command(["pip","install",value])
            library.append(value)

        generate_requirement(self.folder_name, library)

    def _files(self, values):

        default_item = values.get("default",[])
        for value in default_item:
            if "file" in value:
                file = value["file"]
                data = self._curl(f"{self.path}/{file}")
                if data.status_code == 200:
                    write_file_content(self.directory,self.folder_name,file,data.text)
                else:
                    print(f"error in downloading the file {file}")
