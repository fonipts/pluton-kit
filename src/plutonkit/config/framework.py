"""Module providing a function printing python version."""

from plutonkit.management.format import format_argument
from plutonkit.config.package import DOCKER_SETUP,DOCKER_SETUP_DB_TYPE

FRAMEWORK_WEB = [
    format_argument("framework","package_django","Do you need docker","django",DOCKER_SETUP_DB_TYPE),
    format_argument("framework","package_django_rest","Do you need docker","django rest framework",DOCKER_SETUP_DB_TYPE),
    format_argument("framework","package_bottle","Do you need docker","bottle",DOCKER_SETUP),
    format_argument("framework","package_fastapi","Do you need docker","fastapi",DOCKER_SETUP),
    format_argument("framework","package_flask","Do you need docker","flask",DOCKER_SETUP),
]

FRAMEWORK_GRAPHQL = [
    format_argument("framework","package_graphene","Do you need docker","graphene",DOCKER_SETUP),
    format_argument("framework","package_ariadne","Do you need docker","ariadne",DOCKER_SETUP),
    format_argument("framework","package_tartiflette","Do you need docker","tartiflette",DOCKER_SETUP),
    format_argument("framework","package_django_graphbox","Do you need docker","django-graphbox",[]),
]

DEFAULT_GRPC = [
    format_argument("framework","package_default_grpc","Do you need docker","default",DOCKER_SETUP),
]

DEFAULT_WEB3 = [
    format_argument("framework","package_default_web3","Do you need docker","default",DOCKER_SETUP),
]

DEFAULT_WEB_SOCKET = [
    format_argument("framework","package_default_websocket","Do you need docker","default",DOCKER_SETUP),
]
STANDARD_LIBRARY = [
    'pylint==3.0.2',
    'pytest==7.4.3',
    'python-decouple==3.8'
]
SUPPORT_LIBRARY_OTHERS =[
    'Django==4.2.7'
]

SUPPORT_LIBRARY_DJANGO =[
    'Django==4.2.7'
]

SUPPORT_LIBRARY_DJANGO_REST_FRAMEWORK = [
    'Django==4.1',
    'djangorestframework==3.14.0',
    'markdown==3.5.1',
    'django-filter==23.3'
]

SUPPORT_LIBRARY_BOTTLE =[
    'bottle==0.12.25'
]
SUPPORT_LIBRARY_FAST_API =[
    'fastapi==0.104.1',
    'Pydantic==2.5.2',
    'uvicorn[standard]==0.24.0'
]
SUPPORT_LIBRARY_FLASK =[
    'Flask==3.0.0'
]
SUPPORT_LIBRARY_GRAPHENE =[
    'graphene==3.3'
]
SUPPORT_LIBRARY_ARIADNE =[
    'ariadne==0.21',
    'uvicorn[standard]==0.24.0'
]
SUPPORT_LIBRARY_TARTIFLETTE =[
    'tartiflette-aiohttp==1.4.0'
]
SUPPORT_LIBRARY_DJANGO_GRAPHBOX =[
    'django-graphbox==1.2.9',
    'graphene-file-upload==1.3.0'
]
SUPPORT_LIBRARY_GRPC =[
    'grpcio-tools==1.59.2',
    'grpcio==1.59.2'

]
SUPPORT_LIBRARY_WEB_SOCKET =[

]

SUPPORT_LIBRARY_WEB3 = [
    "web3==6.11.3"
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
