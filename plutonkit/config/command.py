"""Module providing a function printing python version."""

from plutonkit.command.action.command import Command
from plutonkit.command.action.create_achitecture import CreateAchitecture
from plutonkit.command.action.create_project import CreateProject
from plutonkit.command.action.review_blueprint import ReviewBlueprint

ACTIONS = {
    "create_achitecture": CreateAchitecture(),
    "create_project": CreateProject(),
    "cmd": Command(),
    "test_blueprint": ReviewBlueprint(),
}
