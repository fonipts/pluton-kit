import os
import sys

from yaml import Loader, load

from plutonkit.config import ARCHITECTURE_DETAILS_FILE
from plutonkit.management.request.ArchitectureRequest import (
    ArchitectureRequest,
)


class ReviewBlueprint:
    def __init__(self) -> None:
        pass

    def comment(self):
        return "Check your blueprint before issue before deploying"

    def execute(self):
        command_list = sys.argv[2 : :] 
        if len(command_list)>0:
            path = command_list[0]
            directory = os.getcwd()
            arch_req = ArchitectureRequest(path, directory)
            if arch_req.isValidReq:
                try:
                    content = load(str(arch_req.getValidReq), Loader=Loader)
                    print(content)
                except Exception as e:
                    print(f"Invalid {ARCHITECTURE_DETAILS_FILE}, please use proper yaml format")
                    sys.exit(0)
        else:
            print("Please specify director , url or git location")
        sys.exit(0)
