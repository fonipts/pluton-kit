import os

from plutonkit.config import REQUIREMENT
from plutonkit.config.framework import STANDARD_LIBRARY

from ....helper.filesystem import default_project_name


def pip_generate_requirement(project_name, library=None):
    directory = os.getcwd()
    with open(
        os.path.join(directory, default_project_name(project_name), REQUIREMENT),
        "w",
        encoding="utf-8",
    ) as fw:
        fw.write("\n".join(STANDARD_LIBRARY + library + [""]))
        fw.close()
