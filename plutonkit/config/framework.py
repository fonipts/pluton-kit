from plutonkit.model.dataclass.format_argument_input import FormatArgumentInput

FRAMEWORK_WEB = [
    FormatArgumentInput(
        type="framework", name="django", question="", option_name="django", config=[]
    ),
    FormatArgumentInput(type="framework", name="bottle", question="", option_name="bottle", config=[]),
    FormatArgumentInput(type="framework", name="fastapi", question="", option_name="fastapi", config=[]),
    FormatArgumentInput(type="framework", name="flask", question="", option_name="flask", config=[]),
]

FRAMEWORK_GRAPHQL = [
    FormatArgumentInput(
        type="framework", name="graphene", question="", option_name="graphene", config=[]
    ),
    FormatArgumentInput(type="framework", name="ariadne", question="", option_name="ariadne", config=[]),
    FormatArgumentInput(
        type="framework", name="tartiflette", question="", option_name="tartiflette", config=[]
    ),
]

DEFAULT_GRPC = [
    FormatArgumentInput(
        type="framework", name="default_grpc", question="", option_name="default", config=[]
    ),
]

DEFAULT_WEB3 = [
    FormatArgumentInput(
        type="framework", name="default_web3", question="", option_name="default", config=[]
    ),
]

DEFAULT_PACKAGE = [
    FormatArgumentInput(
        type="framework", name="default_starter_python", question="Start creating your new python apps", option_name="Python starter", config=[]
    ),
    FormatArgumentInput(
        type="framework", name="default_starter_golang", question="Start creating your new go apps", option_name="Golang starter", config=[]
    ),
    FormatArgumentInput(
        type="framework", name="default_starter_ruby", question="Start creating your new ruby apps", option_name="Ruby starter", config=[]
    ),
]

DEFAULT_WEB_SOCKET = [
    FormatArgumentInput(
        type="framework", name="default_websocket", question="", option_name="default", config=[]
    ),
]

VAR_DEFAULT_BLUEPRINT = [
    "django",
    "bottle",
    "fastapi",
    "flask",
    "graphene",
    "ariadne",
    "tartiflette",
    "default_grpc",
    "default_web3",
    "default_starter_python",
    "default_starter_golang",
    "default_starter_ruby",
    "default_websocket"
]
