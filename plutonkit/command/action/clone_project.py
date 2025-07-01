import os
import sys

from yaml import Loader, load

from plutonkit.config import PROJECT_DETAILS_FILE
from plutonkit.framework.blueprint.generate_blueprint import FrameworkBluePrint
from plutonkit.framework.exception.validation_exception import (
    ValidationException,
)
from plutonkit.framework.request.ArchitectureRequest import ArchitectureRequest
from plutonkit.helper.arguments import get_arg_cmd_value


class CloneProject:
    def __init__(self, argv) -> None:
        self.argv = argv

    def comment(self):
        return "Clone your project from project.yaml file"

    def execute(self):

        option_cmd = self.argv[2::]
        if len(option_cmd) > 0:
            view_extra_cmd = get_arg_cmd_value(option_cmd)
            if "source" in view_extra_cmd:
                self.acces_lobby_blueprint(view_extra_cmd["source"])
            else:
                raise ValidationException("Please use the source as default\n`plutonkit clone_project source=<source of project.yaml>")
        else:
            raise ValidationException("`plutonkit clone_project source=<source of project.yaml> ")

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
            raise ValidationException(arch_req.errorMessage)

    def project_details_execute(self, remote_blueprint,inquiry_val):

        project_name = input("Name of folder project?")

        if len(project_name) <3:
            print("Please specify atleast three char")
            sys.exit(0)

        inquiry_val["folder_name"] = project_name
        framework_blueprint = FrameworkBluePrint(remote_blueprint)
        framework_blueprint.set_folder_name(project_name)
        framework_blueprint.execute_clone_project(inquiry_val)
        sys.exit(0)
