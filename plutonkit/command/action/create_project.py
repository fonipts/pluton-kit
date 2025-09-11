import os
import sys

from yaml import Loader, load

from plutonkit.config import PROJECT_DETAILS_FILE, REMOTE_URL_RAW
from plutonkit.config.framework import VAR_DEFAULT_BLUEPRINT
from plutonkit.config.system import SERVICE_TYPE
from plutonkit.framework.blueprint.generate_blueprint import FrameworkBluePrint
from plutonkit.framework.exception.validation_exception import (
    ValidationException,
)
from plutonkit.framework.request.architecture_request import (
    ArchitectureRequest,
)
from plutonkit.helper.arguments import (
    check_if_default_name, get_arg_cmd_value, get_config,
)
from plutonkit.helper.format import git_name


class CreateProject:
    def __init__(self, argv) -> None:
        self.argv = argv

    def comment(self):
        return f"Start creating your project in our listed framework or clone if you have {PROJECT_DETAILS_FILE} in source directory"

    def execute(self):

        option_cmd = self.argv[2::]
        if len(option_cmd) > 0:
            view_extra_cmd = get_arg_cmd_value(option_cmd)
            if "source" in view_extra_cmd:
                self.acces_lobby_blueprint(view_extra_cmd["source"])
            else:
                raise ValidationException("Please use the source as default\n`plutonkit create_project source=<source directory of architecture.yaml or {PROJECT_DETAILS_FILE}>")

        else:
            self.execute_create_project()

    def acces_lobby_blueprint(self,path):

        directory = os.getcwd()
        arch_req = ArchitectureRequest(path, directory,PROJECT_DETAILS_FILE)
        if arch_req.isValidReq:
            try:
                content = load(str(arch_req.getValidReq), Loader=Loader)

                if content is not None:
                    self.project_details_execute(content.get("blueprint", ""), content.get("default_choices", {}))
                else:
                    print(f"Invalid {PROJECT_DETAILS_FILE}, content is empty or not loaded properly")
                    sys.exit(1)
            except Exception as e:
                print(e, f"Invalid {PROJECT_DETAILS_FILE}, please use proper yaml format")
                sys.exit(1)
        else:
            self.execute_create_project()

    def execute_create_project(self):

        option_cmd = self.argv[2::]
        if len(option_cmd) > 0:
            view_extra_cmd = get_arg_cmd_value(option_cmd)
            if "source" in view_extra_cmd:
                source_name = view_extra_cmd["source"]
                if check_if_default_name(source_name):
                    self.project_details_execute(source_name)
                else:
                    self.git_lobby_bluprint(source_name)
            else:
                raise ValidationException("Please use the source as default\n`plutonkit create_project source=<source directory of architecture.yaml>")
        else:
            self.acces_lobby_blueprint_new_project()

    def acces_lobby_blueprint_new_project(self):

        details_command = {"details": {}, "command": []}
        self.callback_execute(
                details_command, "What is your service type?", SERVICE_TYPE
            )

    def git_lobby_bluprint(self, name):
        clean_name = git_name(name)
        try:
            details_value = VAR_DEFAULT_BLUEPRINT[VAR_DEFAULT_BLUEPRINT.index(clean_name)]
            self.project_details_execute(f"{REMOTE_URL_RAW}/{details_value}")
        except ValueError:
            self.project_details_execute(f"https://github.com/{clean_name}.git")
        except KeyError:
            self.project_details_execute(f"https://github.com/{clean_name}.git")

    def callback_execute(self, reference_value, name, step):

        enum_action = [
            f"{key + 1}  {val.get('option_name')}"
            for key, val in enumerate(step)
        ]
        join_enum_action = "\n".join(enum_action)
        print(f"\n{name}\n{join_enum_action} ")
        answer_step = "1" if len(step) == 1 else f"1-{str(len(step))}"
        answer = input(f"choose only at [{answer_step}]")
        int_answer = int(answer)
        available_step = step[int_answer - 1]
        reference_value["command"].append(
                {
                    "name": available_step["name"],
                    "type": available_step["type"],
                    "field_type": available_step["field_type"],
                }
            )

        if len(available_step["config"]) > 0:
            self.callback_execute(
                reference_value,
                available_step["question"],
                available_step["config"],
            )
        else:
            self.query_execute(reference_value)

    def query_execute(self, reference_value):

        command_value = get_config(reference_value)
        framework = command_value.get("framework", "")
        remote_blueprint = f"{REMOTE_URL_RAW}/{framework}"
        self.project_details_execute(remote_blueprint)

    def project_details_execute(self, remote_blueprint,inquiry_val=None):

        project_name = input("Name of folder project?")
        if len(project_name) <3:
            print("Please specify atleast three char")
            sys.exit(0)
        framework_blueprint = FrameworkBluePrint(remote_blueprint)
        framework_blueprint.set_folder_name(project_name)
        if inquiry_val:
            inquiry_val["folder_name"] = project_name
            framework_blueprint.execute_clone_project(inquiry_val)
        else:
            framework_blueprint.execute_create_project()
        sys.exit(0)
