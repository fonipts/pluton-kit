"""Module providing a function printing python version."""

from plutonkit.command.action.command import Command
from plutonkit.command.action.create_achitecture import CreateAchitecture
from plutonkit.command.action.create_project import CreateProject
from plutonkit.command.action.validate_blueprint import ValidateBlueprint

ACTIONS = {
    "create_achitecture": CreateAchitecture(),
    "create_project": CreateProject(),
    "cmd": Command(),
    "validate_blueprint": ValidateBlueprint(),
}
