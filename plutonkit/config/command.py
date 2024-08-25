"""Module providing a function printing python version."""

from plutonkit.command.action.command import Command
from plutonkit.command.action.create_project import CreateProject
from plutonkit.command.action.test import Test

ACTIONS = {
    "create_project": CreateProject(),
    "cmd": Command(),
    "test": Test(),
}
