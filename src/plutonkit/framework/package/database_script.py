import re
from plutonkit.config.framework import (SUPPORT_LIBRARY_FLASK_SQL_ALCHEMY,
SUPPORT_LIBRARY_SQL_ALCHEMY,
SUPPORT_LIBRARY_SQL_POSTGRE,
SUPPORT_LIBRARY_SQL_MYSQL)

class DatabaseScript:
    def __init__(self,framework,db_package,db_type) -> None:
        self.framework = framework
        self.db_package = db_package
        self.db_type = db_type
    def __isFlaskDb(self):
        return self.framework == "package_flask" and self.db_package == "package_sqlalchemy"
    def getContent(self):

        if self.db_package == "package_sqlalchemy":
            database_uri =""
            if self.db_type == "db_sqlite":
                database_uri = "sqlite:///test.sqlite"
            if self.db_type == "db_mysql":
                database_uri ="'mysql://%s:%s@%s/%s'%(config('DB_USER'),quote_plus(config('DB_PASSWORD')),config('DB_CONNECTION'),config('DB_NAME'))"
            if self.db_type == "db_postgresql":
                database_uri ="'postgresql+psycopg://%s:%s@%s/%s'%(config('DB_USER'),quote_plus(config('DB_PASSWORD')),config('DB_CONNECTION'),config('DB_NAME'))"

            if self.framework == "package_flask":

                return """
db = SQLAlchemy()
#noqa: create the app
app = Flask(__name__)
#noqa: configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = %s
#noqa: initialize the app with the extension
db.init_app(app)
"""%(database_uri)

            return """
engine = create_engine(%s)
conn = engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
"""%(database_uri)

        if self.framework == "django":
                if self.db_type == "db_mysql":
                    pass
                if self.db_type == "db_postgresql":
                    pass

        return ""

    def getImport(self):

        if self.db_package == "package_sqlalchemy":
            if self.framework == "package_flask":

                return "\n".join([
                    "from flask_sqlalchemy import SQLAlchemy",
                    "from sqlalchemy.orm import declarative_base,sessionmaker",
                    "from decouple import config",
                    "from urllib.parse import quote_plus"
                ])
            return "\n".join([
                    "from sqlalchemy import create_engine",
                    "from sqlalchemy.orm import declarative_base,sessionmaker",
                    "from decouple import config",
                    "from urllib.parse import quote_plus"
                ])
        if self.framework == "django":
            return "\n".join([
                    "from decouple import config",
                    "from urllib.parse import quote_plus"
                ])
        return ""

    def getRequirement(self):

        imprt = []
        if self.db_package == "package_sqlalchemy":
            imprt = SUPPORT_LIBRARY_SQL_ALCHEMY
        if self.__isFlaskDb():
            imprt = SUPPORT_LIBRARY_FLASK_SQL_ALCHEMY
        if self.db_type == "db_mysql":
            imprt += SUPPORT_LIBRARY_SQL_MYSQL
        if self.db_type == "db_postgresql":
            imprt += SUPPORT_LIBRARY_SQL_POSTGRE
        return imprt
