from plutonkit.config.command import ACTIONS

class Help:
    def __init__(self) -> None:
        pass

    def comment(self):
        return "To see all available commands"
    def execute(self):
        template = "Here are the available commands you can used\n"\
            "Commands:\n"
        for key,val in ACTIONS.items():
            template += "\t(%s) %s\n"%(key,val.comment())
        print(template)