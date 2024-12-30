from plutonkit.command.action.clone_project import CloneProject
from plutonkit.command.action.command import Command
from plutonkit.command.action.create_achitecture import CreateAchitecture
from plutonkit.command.action.create_project import CreateProject
from plutonkit.command.action.help import Help
from plutonkit.command.action.validate_blueprint import ValidateBlueprint

test_arg = []


clone_project = CloneProject(test_arg)
command =Command(test_arg)
create_achitecture = CreateAchitecture(test_arg)
create_project = CreateProject(test_arg)
help = Help(test_arg)
validate_blueprint = ValidateBlueprint(test_arg)
