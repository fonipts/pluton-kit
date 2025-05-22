PROJECT_COMMAND_FILE: str = "command.yaml"
PROJECT_DETAILS_FILE: str = "project.yaml"
ARCHITECTURE_DETAILS_FILE: str = "architecture.yaml"
PYTHON_CMD:str="command"
PYTHON_BLUEPRINT:str="blueprint"
#REMOTE_URL_RAW: str = "https://raw.githubusercontent.com/fonipts/pluton-lobby/main/blueprint"
REMOTE_URL_RAW: str = "https://raw.githubusercontent.com/fonipts/pluton-lobby/refs/heads/dev/1.0.32a1/blueprint"

INTRODUCTION: str = (
    "Welcome to pluton-kit, this is your application builder in python woorld"
)

ARCHITECTURE_REQUEST_ERROR_MESSAGE = "`source` in blueprint was invalid, please check and try again later"

SEARCH_CHAR_ENCLOSE = [

    {
        "name":"double_qoute",
        "regex":r'\"',
        "value":'"'
    },
    {
        "name":"single_qoute",
        "regex":r"\'",
        "value":"'"
    },
    {
        "name":"back_qoute",
        "regex":r"\`",
        "value":"`"
    }
]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
