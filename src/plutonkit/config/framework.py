"""Module providing a function printing python version."""

from plutonkit.management.format import format_argument_input

FRAMEWORK_WEB = [
    format_argument_input("framework", "django", "Do you need docker", "django", []),
    format_argument_input("framework", "bottle", "Do you need docker", "bottle", []),
    format_argument_input("framework", "fastapi", "Do you need docker", "fastapi", []),
    format_argument_input("framework", "flask", "Do you need docker", "flask", []),
]

FRAMEWORK_GRAPHQL = [
    format_argument_input(
        "framework", "graphene", "Do you need docker", "graphene", []
    ),
    format_argument_input("framework", "ariadne", "Do you need docker", "ariadne", []),
    format_argument_input(
        "framework", "tartiflette", "Do you need docker", "tartiflette", []
    ),
]

DEFAULT_GRPC = [
    format_argument_input(
        "framework", "default_grpc", "Do you need docker", "default", []
    ),
]

DEFAULT_WEB3 = [
    format_argument_input(
        "framework", "default_web3", "Do you need docker", "default", []
    ),
]

DEFAULT_PACKAGE = [
    format_argument_input(
        "framework", "default_packaging", "Start creating your new apps", "default", []
    ),
]

DEFAULT_WEB_SOCKET = [
    format_argument_input(
        "framework", "default_websocket", "Do you need docker", "default", []
    ),
]

STANDARD_LIBRARY = ["pylint==3.0.2", "pytest==7.4.3", "python-decouple==3.8"]
