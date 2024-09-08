import os
import sys

from yaml import Loader, load

from plutonkit.config import PROJECT_DETAILS_FILE, REMOTE_URL_RAW
from plutonkit.config.system import SERVICE_TYPE
from plutonkit.framework.blueprint import FrameworkBluePrint
from plutonkit.helper.config import get_config


class CreateProject:
    def __init__(self, argv) -> None:
        self.argv = argv

    def comment(self):
        return "Start creating your project in our listed framework"

    def execute(self):

        option_cmd = self.argv[2::]
        if len(option_cmd) > 0:
            view_extra_cmd = self._get_arg_value(option_cmd)
            if "source" in view_extra_cmd:
                self.project_details_execute(view_extra_cmd["source"])
            else:
                print("Please use the source as default\n")
                print("`plutonkit create_project source=<source of blueprint> ")
                sys.exit(0)
        else:
            self.acces_lobby_blueprint()

    def acces_lobby_blueprint(self):

        directory = os.getcwd()
        path = os.path.join(directory, PROJECT_DETAILS_FILE)
        if os.path.exists(path):
            is_file = os.path.isfile(path)
            if is_file:

                try:
                    with open(path, "r", encoding="utf-8") as fi:
                        read = fi.read()
                        content = load(str(read), Loader=Loader)
                        remote_blueprint = content.get("blueprint")
                        self.project_details_execute(remote_blueprint)
                except Exception as e:
                    print(e)
                    print("Invalid yaml file content")
                    sys.exit(0)

        else:

            details_command = {"details": {}, "command": []}
            self.callback_execute(
                details_command, "What is your service type?", SERVICE_TYPE
            )

    def callback_execute(self, reference_value, name, step):

        try:
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
        except Exception:
            print(f"Invalid argument please select in the available command `{answer}`\n")

    def query_execute(self, reference_value):

        command_value = get_config(reference_value)
        framework = command_value.get("framework", "")
        remote_blueprint = f"{REMOTE_URL_RAW}/{framework}"
        self.project_details_execute(remote_blueprint)

    def project_details_execute(self, remote_blueprint):

        project_name = input("Name of folder project?")
        folder_name = f"Project name: {project_name}"
        answer = input(f"\n{folder_name}\nDo you want to proceed installation process?(y/n) > ")
        if answer == "y":

            framework_blueprint = FrameworkBluePrint(remote_blueprint)
            framework_blueprint.set_folder_name(project_name)
            framework_blueprint.execute()
            sys.exit(0)
        else:
            print("Your confirmation say `No`")
            sys.exit(0)

    def _get_arg_value(self, args):
        local_obj = {}
        local_obj["extra"] = []

        for val in args:
            word_split = val.split("=")

            if len(word_split) > 0:
                local_obj[word_split[0]] = "=".join(word_split[1::])
            else:
                local_obj["extra"].append(val)

        return local_obj
