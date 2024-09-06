import os
import sys

from yaml import Loader, load

from plutonkit.config import ARCHITECTURE_DETAILS_FILE
from plutonkit.management.request.ArchitectureRequest import (
    ArchitectureRequest,
)


class CreateAchitecture:
    def __init__(self) -> None:
        pass

    def comment(self):
        return "Create your first architecture"

    def execute(self):
         
        project_name = input("Name of folder project?")
        folder_name = f"Project name: {project_name}"
        answer = input(f"\n{folder_name}\nDo you want to proceed creating your starterkit?(y/n) > " )
        if answer == "y":
            pass
        sys.exit(0)
