"""Module providing a function printing python version."""

from plutonkit.management.format import format_argument_input

DATABASE_TYPE = [
    format_argument_input("db_type","db_sqlite","What is sqlite","sqlite",[]),
    format_argument_input("db_type","db_postgresql","What is postgresql","postgresql",[]),
    format_argument_input("db_type","db_mysql","What is mysql","mysql",[])
]
DATABASE_PACKAGE = [
    format_argument_input("db_package","package_db_none","No package","db_none",[]),
    format_argument_input("db_package","package_sqlalchemy","Your sqlalchemy is your default SQL package","sqlalchemy",DATABASE_TYPE)
]

DOCKER_IMAGE_TYPE = [
    format_argument_input("docker_image_type","docker_image_python","Your Database library","python",DATABASE_PACKAGE),
    format_argument_input("docker_image_type","docker_image_nginx","Your Database library","nginx",DATABASE_PACKAGE),
    format_argument_input("docker_image_type","docker_image_apache","Your Database library","apache",DATABASE_PACKAGE),
]

DOCKER_SETUP = [
    format_argument_input("docker","default_docker_yes","Your Docker image","yes",DOCKER_IMAGE_TYPE),
    format_argument_input("docker","default_docker_no","Your Database library","no",DATABASE_PACKAGE),
]

DOCKER_SETUP_DB_TYPE = [
    format_argument_input("docker","default_docker_yes","Your Docker image","yes",DOCKER_IMAGE_TYPE),
    format_argument_input("docker","default_docker_no","Your Database library","no",DATABASE_TYPE),
]

