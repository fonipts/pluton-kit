"""Module providing a function printing python version."""

import sys

from plutonkit.config.command import ACTIONS


class Help:
    def __init__(self) -> None:
        pass

    def comment(self):
        return "To see all available commands"

    def execute(self):
        template = "Here are the available commands you can used\nCommands:\n"

        for key, val in ACTIONS.items():
            template += f"\t({key}) {val.comment()}\n"
        print(template)
        sys.exit(0)
