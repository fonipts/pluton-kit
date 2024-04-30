"""Module providing a function printing python version."""

from plutonkit.management.format import format_argument_input
from plutonkit.config.package import DOCKER_SETUP,DOCKER_SETUP_DB_TYPE

FRAMEWORK_WEB = [
    format_argument_input("framework","django","Do you need docker","django",[]),
    format_argument_input("framework","django_rest","Do you need docker","django rest framework",[]),
    format_argument_input("framework","bottle","Do you need docker","bottle",[]),
    format_argument_input("framework","fastapi","Do you need docker","fastapi",[]),
    format_argument_input("framework","flask","Do you need docker","flask",[]),
]

FRAMEWORK_GRAPHQL = [
    format_argument_input("framework","graphene","Do you need docker","graphene",[]),
    format_argument_input("framework","ariadne","Do you need docker","ariadne",[]),
    format_argument_input("framework","tartiflette","Do you need docker","tartiflette",[]),
    format_argument_input("framework","django_graphbox","Do you need docker","django-graphbox",[]),
]

DEFAULT_GRPC = [
    format_argument_input("framework","default_grpc","Do you need docker","default",[]),
    format_argument_input("framework","default_grpc_w_interceptor","Do you need docker","with interceptor auth support",[]),
]

DEFAULT_WEB3 = [
    format_argument_input("framework","default_web3","Do you need docker","default",[]),
]

DEFAULT_PACKAGE = [
    format_argument_input("framework","default_packaging","Start creating your new apps","default",[]),
]

DEFAULT_WEB_SOCKET = [
    format_argument_input("framework","default_websocket","Do you need docker","default",[]),
]

STANDARD_LIBRARY = [
    "pylint==3.0.2",
    "pytest==7.4.3",
    "python-decouple==3.8"
]

SUPPORT_LIBRARY_FLASK_SQL_ALCHEMY = [
    "Flask-SQLAlchemy==3.1.1"
]

SUPPORT_LIBRARY_SQL_ALCHEMY = [
    "SQLAlchemy==2.0.23"
]

SUPPORT_LIBRARY_SQL_POSTGRE = [
    "psycopg[binary,pool]==3.1.14"
]

SUPPORT_LIBRARY_SQL_MYSQL = [
    "PyMySQL==1.1.0"
]
