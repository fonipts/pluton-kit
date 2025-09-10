import importlib
import os
import sys
from typing import Any, List, Optional, Union

from yaml import Loader, load

from plutonkit.config import (
    PROJECT_COMMAND_FILE, PROJECT_DETAILS_FILE, PYTHON_BLUEPRINT, bcolors,
)
from plutonkit.framework.command.py_validate_content import PyValidateContent
from plutonkit.framework.exception.warning_exception import WarningException
from plutonkit.framework.filesystem.blueprint_file_schema import (
    BlueprintFileSchema,
)
from plutonkit.framework.request.architecture_request import (
    ArchitectureRequest,
)
from plutonkit.framework.request.file_request import FileRequest
from plutonkit.framework.terminal.inquiry_terminal import InquiryTerminal
from plutonkit.framework.tymplu.condition.condition_delimiter import (
    ConditionDelimiter,
)
from plutonkit.framework.tymplu.condition.condition_identify import (
    ConditionIdentify,
)
from plutonkit.helper.command import clean_command_split, pip_run_command
from plutonkit.helper.environment import setEnvironmentVariable
from plutonkit.helper.filesystem import (
    create_yaml_file, generate_project_folder_cwd, write_file_content,
)
from plutonkit.helper.template import convert_shortcode


class FrameworkBluePrint:
    def __init__(self, path) -> None:
        self.path = path
        self.folder_name = ""
        self.directory = os.getcwd()
        self.arch_req:Optional[ArchitectureRequest] = None
        self.blueprint_file:Optional[FileRequest] = None

        self.local_block = {}
        self.local_bootscript = []
        self.bootscript_run:Union[Any, None] = None

    def set_folder_name(self, name):
        self.folder_name = name

    def execute_clone_project(self,ans_ref):
        self.blueprint_file = FileRequest(self.path, self.directory, f"{PYTHON_BLUEPRINT}.py")
        self.arch_req = ArchitectureRequest(self.path, self.directory)
        if self.arch_req.isValidReq is False:
            print(self.arch_req.errorMessage)

            self.arch_req.clearRepoFolder()
            sys.exit(0)
        try:
            generate_project_folder_cwd(self.folder_name)
            content = load(str(self.arch_req.getValidReq), Loader=Loader)
            self._bootloader_project(content,ans_ref)

        except Exception as e:
            print(e)
            print(f"{bcolors.FAIL}Invalid details to proceed in creating new project{bcolors.ENDC}")
            sys.exit(0)

    def execute_create_project(self):
        self.blueprint_file = FileRequest(self.path, self.directory, f"{PYTHON_BLUEPRINT}.py")
        self.arch_req = ArchitectureRequest(self.path, self.directory)
        if self.arch_req.isValidReq is False:
            print(f"{bcolors.FAIL}{self.arch_req.errorMessage}{bcolors.ENDC}")

            self.arch_req.clearRepoFolder()
            sys.exit(0)
        try:
            generate_project_folder_cwd(self.folder_name)

            content:Union[Any]= load(str(self.arch_req.getValidReq), Loader=Loader)

            choices:List[Any] = content.get("choices", [])

            inquiry_terminal = InquiryTerminal(choices)
            inquiry_terminal.execute()

            while inquiry_terminal.is_continue():

                if inquiry_terminal.is_terminate():
                    self._bootloader_project(content,inquiry_terminal.get_answer())
                    break
        except WarningException as e:
            raise WarningException(e.message) from e

        except Exception as e:
            print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Invalid details to proceed in creating new project{bcolors.ENDC}")
            self.arch_req.clearRepoFolder()

            sys.exit(0)

    def _review_blueprint_script(self):
        cmd_file = f"{PYTHON_BLUEPRINT}.py"
        get_filename = ""
        get_dir = ""
        is_valid_req = False
        if self.blueprint_file is not None:
            get_filename = self.blueprint_file.getFilename()
            get_dir = self.blueprint_file.getDir()
            is_valid_req = self.blueprint_file.IsValidReq()


        if os.path.exists(str(get_filename)) and is_valid_req:
            py_file_class = PyValidateContent(str(get_filename))
            var_class_import = py_file_class.get_class_import()

            if var_class_import.get("Blueprint",None) is None:
                raise WarningException(f"In your `{cmd_file}`, please import `Blueprint` in your blueprint.py")

            var_class_call = py_file_class.get_class_call()

            if var_class_import["Blueprint"] not in var_class_call:
                raise WarningException(f"In your `{cmd_file}`, please use `Blueprint` as class in your blueprint.py for you to use block and script")

            if get_dir is not None:
                sys.path.append(get_dir)
            mod = importlib.import_module(PYTHON_BLUEPRINT)

            blueprint_class = getattr(mod, var_class_call[ var_class_import["Blueprint"] ])

            if not hasattr(blueprint_class,"get_execute"):
                raise WarningException(f"In your `{cmd_file}`, please use `from plutonkit import Blueprint` in your blueprint.py")

            get_execute = blueprint_class.get_execute()

            self.local_block = get_execute["block"]
            if py_file_class.is_run_func_available():
                self.bootscript_run = mod

    def _bootloader_project(self, content, args):
        files = content.get("files", [])
        script = content.get("script", {})
        bootscript = content.get("bootscript", [])
        env = content.get("env",{})
        setEnvironmentVariable(env)
        terminal_answer = args
        terminal_answer["folder_name"] = self.folder_name

        self._review_blueprint_script()

        self._files(files, terminal_answer)
        self._boot_command(bootscript, terminal_answer)
        os.chdir(self.directory)
        create_yaml_file(
            self.folder_name,
            PROJECT_DETAILS_FILE,
            {"name": self.folder_name, "blueprint": self.path, "default_choices": terminal_answer},
            )
        create_yaml_file(
            self.folder_name, PROJECT_COMMAND_FILE, {"script": self._script_template(script,terminal_answer), "env": env}
            )
        if self.arch_req is not None:
            self.arch_req.clearRepoFolder()
        if self.blueprint_file is not None:
            self.blueprint_file.deleteFile()

        print(f"{bcolors.OKGREEN}Congrats!! your first project has been generated{bcolors.ENDC}")

    def _script_template(self,configs,args):
        for value in configs:
            commands = configs[value]['command']
            for key_com,val_com in enumerate(commands):
                commands[key_com] = convert_shortcode(val_com, args)
        return configs

    def _files(self, values, args):

        files_check: list[BlueprintFileSchema] = []
        default_item = values.get("default", [])

        for value in default_item:
            if self.arch_req is not None:
                for file1 in self.arch_req.getBlob(value):
                    files_check.append(BlueprintFileSchema(file1, args))

        optional_item = values.get("optional", [])
        for value in optional_item:

            #
            cond = ConditionDelimiter(value.get("condition"))
            cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording,args)


            if "dependent" in value and cond_valid.validate():
                for s_value in value["dependent"]:
                    if self.arch_req is not None:
                        for file1 in self.arch_req.getBlob(s_value):

                            files_check.append(BlueprintFileSchema(file1, args))

        for value in files_check:
            if value.isObjFile():
                if self.arch_req is not None:
                    data = self.arch_req.getFiles(value.value["file"])
                    if data["is_valid"]:
                        for save_file in value.get_save_files():
                            write_file_content(
                                self.directory, self.folder_name, save_file, data["content"], args, self.local_block
                            )
                    else:
                        print(f"{bcolors.FAIL}error in downloading the file {value.value['file']}{bcolors.ENDC}")

    def _boot_command(self, values, args):

        path = os.path.join(self.directory, self.folder_name)

        is_exec_running = len(values)>0
        while is_exec_running:
            chdir = os.path.join(path,convert_shortcode(values[0].get("chdir",""), args))
            command = values[0].get("command", "")
            condition = values[0].get("condition", "")
            str_convert = convert_shortcode(command, args)

            is_valid = False
            if condition == "":
                is_valid = True
            else:

                cond = ConditionDelimiter(condition)
                cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording,args)
                is_valid = cond_valid.validate()

            if is_valid:
                os.chdir(chdir)
                try:
                    pip_run_command(clean_command_split(str_convert))
                except Exception as E:
                    print(E)
            values.pop(0)
            is_exec_running = len(values)>0
        try:
            if self.bootscript_run is not None:
                self.bootscript_run.run(args)
        except Exception as E:
            raise WarningException(E) from E
