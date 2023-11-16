from plutonkit.core.helper.format import format_argument

DATABASE_TYPE = [
    format_argument("db_type","db_postgresql","What is postgresql","postgresql",[]),
    format_argument("db_type","db_mysql","What is mysql","mysql",[])
]
DATABASE_PACKAGE = [
    format_argument("db_package","package_sqlalchemy","Your sqlalchemy is your default SQL package","sqlalchemy",DATABASE_TYPE)
]

DOCKER_SETUP = [
    format_argument("docker","default_docker_yes","Your Database library","yes",DATABASE_PACKAGE),
    format_argument("docker","default_docker_no","Your Database library","no",DATABASE_PACKAGE),
]

DOCKER_SETUP_NO_DB = [
    format_argument("docker","default_docker_yes","Your Database library","yes",[]),
    format_argument("docker","default_docker_no","Your Database library","no",[]),
]
