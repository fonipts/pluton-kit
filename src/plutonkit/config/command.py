"""Module providing a function printing python version."""

from plutonkit.command.action.command import Command
from plutonkit.command.action.create_project import CreateProject

ACTIONS = {
    "create_project": CreateProject(),
    "cmd": Command(),
}
