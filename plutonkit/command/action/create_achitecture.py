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
         
        print("Please specify director , url or git location")
        sys.exit(0)
