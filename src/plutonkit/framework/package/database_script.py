import re
from plutonkit.config.framework import SUPPORT_LIBRARY_FLASK_SQL_ALCHEMY,\
SUPPORT_LIBRARY_SQL_ALCHEMY,\
SUPPORT_LIBRARY_SQL_POSTGRE,\
SUPPORT_LIBRARY_SQL_MYSQL

class DatabaseScript:
    def __init__(self,framework,db_package,db_type) -> None:
        self.framework = framework
        self.db_package = db_package
        self.db_type = db_type
    def __isFlaskDb(self):
        return self.framework =="package_flask" and self.db_package =="package_sqlalchemy"
    def getContent(self):

        if self.db_package =="package_sqlalchemy":
            database_uri =""
            if self.db_type =="db_mysql":
                database_uri ="mysql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_CONNECTION')}/{config('DB_NAME')}"
            if self.db_type =="db_postgresql":
                database_uri ="postgresql+psycopg://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_CONNECTION')}/{config('DB_NAME')}"

            if self.framework =="package_flask":

                return '''
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "%s"
# initialize the app with the extension
db.init_app(app)
            '''%(database_uri)

            return '''
engine = create_engine("%s")'''%(database_uri)

        if self.framework =="django":
                if self.db_type =="db_mysql":
                    pass
                if self.db_type =="db_postgresql":
                    pass

        return ""

    def getImport(self):

        if self.db_package =="package_sqlalchemy":
            if self.framework =="package_flask":

                return "\n".join([
                    "from flask_sqlalchemy import SQLAlchemy",
                    "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column",
                    "from decouple import config"
                ])
            return "\n".join([
                    "from sqlalchemy import create_engine",
                    "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column",
                    "from decouple import config"
                ])
        if self.framework =="django":
            return "\n".join([
                    "from decouple import config"
                ])
        return ""

    def getRequirement(self):

        imprt = []
        if self.db_package  == "package_db_none":
            imprt = SUPPORT_LIBRARY_SQL_ALCHEMY
        if self.__isFlaskDb():
            imprt = SUPPORT_LIBRARY_FLASK_SQL_ALCHEMY
        if self.db_type =="db_mysql":
            imprt+=SUPPORT_LIBRARY_SQL_MYSQL
        if self.db_type =="db_postgresql":
            imprt+=SUPPORT_LIBRARY_SQL_POSTGRE
        return imprt
