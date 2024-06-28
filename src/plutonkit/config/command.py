"""Module providing a function printing python version."""

from plutonkit.command.action.create_project import CreateProject
from plutonkit.command.action.command import Command

ACTIONS = {
    "create_project": CreateProject(),
    "command": Command(),
}
