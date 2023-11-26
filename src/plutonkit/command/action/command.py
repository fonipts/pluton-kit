import os
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import sys

from plutonkit.helper.command import pip_run_command
from plutonkit.config import PROJECT_COMMAND_FILE

class Command:
    def __init__(self) -> None:
        pass

    def comment(self):
        return "Executing command using plutonkit"
    def execute(self):
        DIRECTORY = os.getcwd()
        path = os.path.join(DIRECTORY, PROJECT_COMMAND_FILE)
        if os.path.exists(path):
            is_file = os.path.isfile(path)
            if is_file:
                with open(path , 'r') as fi:
                    try:
                        read = fi.read()
                        content = load(str(read), Loader=Loader)

                        content_script = content['script']
                        try:
                            command_value = sys.argv[2]
                            if command_value not in content_script:
                                print("Invalid command variable")
                                return

                            try :
                                for val in content_script[command_value]['command']:
                                    os.chdir(DIRECTORY)
                                    pip_run_command(val.split(" "))
                            except Exception as e2:
                                print(e2)
                        except Exception as e1:
                            print("Please specify your command like `plutonkit command start`")
                    except Exception as e:
                        print("Invalid yaml file content",e)
        else:
            print("This command file `%s` is missing in the directory project"%(PROJECT_COMMAND_FILE))

