"""Module providing a function printing python version."""

import os
import sys
import re
import requests
from yaml import Loader, load

from plutonkit.config import (
    ARCHITECTURE_DETAILS_FILE, PROJECT_COMMAND_FILE, PROJECT_DETAILS_FILE,
)
from plutonkit.helper.command import clean_command_split, pip_run_command
from plutonkit.helper.filesystem import (
    create_yaml_file, generate_project_folder_cwd, generate_requirement,
    write_file_content,
)
from plutonkit.helper.template import convert_shortcode
from plutonkit.management.logic.ConditionSplit import ConditionSplit

from .inquiry_terminal import InquiryTerminal


class FrameworkBluePrint:
    def __init__(self, path) -> None:
        self.path = path
        self.folder_name = ""
        self.directory = os.getcwd()

    def set_folder_name(self, name):
        self.folder_name = name

    def execute(self):
        data = self._curl(f"{self.path}/{ARCHITECTURE_DETAILS_FILE}")
        if data.status_code != 200:
            print("Can not access, please try again later")
            sys.exit(0)
        try:
            generate_project_folder_cwd(self.folder_name)
            content = load(str(data.text), Loader=Loader)

            choices = content.get("choices", [])

            inquiry_terminal = InquiryTerminal(choices)
            inquiry_terminal.execute()

            while inquiry_terminal.is_continue():

                if inquiry_terminal.is_terminate():
                    dependencies = content.get("dependencies", [])
                    files = content.get("files", [])
                    script = content.get("script", {})
                    bootscript = content.get("bootscript", [])

                    self._packages(dependencies, inquiry_terminal.get_answer())
                    terminal_answer = inquiry_terminal.get_answer()
                    terminal_answer["folder_name"] = self.folder_name

                    create_yaml_file(
                        self.folder_name,
                        PROJECT_DETAILS_FILE,
                        {"name": self.folder_name, "blueprint": self.path,"default_choices":terminal_answer},
                    )
                    create_yaml_file(
                        self.folder_name, PROJECT_COMMAND_FILE, {"script": script}
                    )
                    self._boot_command(bootscript, "start",terminal_answer)
                    self._files(files, terminal_answer)
                    self._boot_command(bootscript, "end",terminal_answer)
                    print("Congrats!! your first project has been generated")
                    break

        except Exception as e:
            print(e)
            print("Invalid yaml file content")
            sys.exit(0)

    def _curl(self, path):
        data = requests.get(path, timeout=25)
        return data

    def _packages(self, values, args):
        default_item = values.get("default", [])
        library = []
        for value in default_item:
            library.append(value)

        optional_item = values.get("optional", [])
        for value in optional_item:
            cond_valid = ConditionSplit(value.get("condition"), args)
            if "dependent" in value and cond_valid.validCond():
                library += value.get("dependent", [])

        #for value in library:
        #    pip_run_command(["pip", "install", value])
        generate_requirement(self.folder_name, library)

    def _files(self, values, args):

        default_item = values.get("default", [])
        for value in default_item:
            if "file" in value:
                file = value["file"]
                data = self._curl(f"{self.path}/{file}")
                if data.status_code == 200:
                    if "mv_file" in value:
                        file =value["mv_file"]
                        file = re.sub(r"^(/)","",file)
    
                    write_file_content(
                        self.directory, self.folder_name, file, data.text, args
                    )
                else:
                    print(f"error in downloading the file {file}")
        optional_item = values.get("optional", [])
        for value in optional_item:
            cond_valid = ConditionSplit(value.get("condition"), args)

            if "dependent" in value and cond_valid.validCond():
                for s_value in value["dependent"]:
                    if "file" in s_value:
                        file = convert_shortcode(s_value["file"],args)
                        data = self._curl(f"{self.path}/{file}")
                        #if "mv_folder_name" in value:
                        #    file = os.path.join(convert_shortcode(value["mv_folder_name"],args), file)
                        if data.status_code == 200:
                            if "mv_file" in s_value:
                                file = convert_shortcode(s_value["mv_file"],args)
                                file = re.sub(r"^(/)","",file)
                                print ("@@@@@")
                            write_file_content(
                                self.directory, self.folder_name, file, data.text, args
                            )
                        else:
                            print(f"error in downloading the file {file}")

    def _boot_command(self, values,post_exec, args):
        
        path = os.path.join(self.directory, self.folder_name)
        os.chdir(path)
        print(path,"::",post_exec)
        for value in values:
            command = value.get("command", "")
            condition = value.get("condition", "")
            value_exec_position = value.get("exec_position", "end")
            is_valid = False
            if condition == "":
                is_valid = True
            else:
                cond_valid = ConditionSplit(condition, args)
                is_valid = cond_valid.validCond()

            if is_valid and post_exec == value_exec_position:
                str_convert = convert_shortcode(command, args)
                #if "chdir" in value:
                #    os.chdir(os.path.join(path, value["chdir"]))
                pip_run_command(clean_command_split(str_convert))
                #os.chdir(path)
        #os.chdir(os.path.join(directory, "../"))