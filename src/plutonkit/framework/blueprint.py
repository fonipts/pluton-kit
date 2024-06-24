"""Module providing a function printing python version."""

from plutonkit.config import ARCHITECTURE_DETAILS_FILE,PROJECT_COMMAND_FILE,PROJECT_DETAILS_FILE
import requests

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from plutonkit.helper.filesystem import create_yaml_file, generate_project_folder_cwd ,generate_requirement,write_file_content
import yaml

from plutonkit.helper.command import pip_run_command

import os
import sys
from .inquiry_terminal import InquiryTerminal
from plutonkit.management.logic.ConditionIdentify import ConditionIdentify


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

                choices = content.get("choices",[])

                inquiry_terminal = InquiryTerminal(choices)
                inquiry_terminal.execute()

                while inquiry_terminal.isContinue():

                    if inquiry_terminal.isTerminate():
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

                        self._packages(dependencies,inquiry_terminal.getAnswer())
                        self._files(files,inquiry_terminal.getAnswer())
                        print(inquiry_terminal.getAnswer(),":getAnswer")
                        print("Congrats!! your first project has been generated")
                        break
                     
            except Exception as e:
                print(e)
                print("Invalid yaml file content")
                sys.exit(0)
        else:
            print("Can not access, please try again later")

    def _curl(self,path):
        data = requests.get(path)
        return data

    def _packages(self,values,args):
        default_item = values.get("default",[])
        library = []
        for value in default_item:
            pip_run_command(["pip","install",value])
            library.append(value)

        optional_item = values.get("optional",[]) 
        for value in optional_item:
            cond_valid = ConditionIdentify(value.get('condition'), args)
            if "dependent" in value and cond_valid.validCond(): 
                library += value.get("dependent",[])

        generate_requirement(self.folder_name, library)

    def _files(self, values,args):

        default_item = values.get("default",[])
        for value in default_item:
            if "file" in value:
                file = value["file"]
                data = self._curl(f"{self.path}/{file}")
                if data.status_code == 200:
                    write_file_content(self.directory,self.folder_name,file,data.text,args)
                else:
                    print(f"error in downloading the file {file}")
        optional_item = values.get("optional",[]) 
        for value in optional_item:
            cond_valid = ConditionIdentify(value.get('condition'), args)
            if "dependent" in value and cond_valid.validCond(): 
                for s_value in value["dependent"]:
                    if "file" in s_value:
                        file = s_value["file"]      
                        data = self._curl(f"{self.path}/{file}")
                        if data.status_code == 200:
                            write_file_content(self.directory,self.folder_name,file,data.text,args)
                        else:
                            print(f"error in downloading the file {file}")
