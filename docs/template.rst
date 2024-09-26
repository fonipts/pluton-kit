============
Template
============
The goal is to have an idea in building function in template and reuse to if you import to different project.

Most of pass value are coming from choices at ``architecture.yaml``


Functional syntax
----------------
This function syntax will work on *.tpl{ext file} format otherwise it will be ignore in execution.

 .. code-block:: html


   ({   
        @condition{
            database == "postgres"
        }
        @content{
        engine = create_engine(f'postgresql+psycopg://{config("DB_USER")}:{quote_plus(config("DB_PASSWORD"))}@{config("DB_CONNECTION")}/{config("DB_NAME")}')
        conn = engine.connect()
        Base = declarative_base()
        Session = sessionmaker(bind=engine)
        session = Session()

        }
        @end{}
        @condition{
            database == "mysql"
        }
        @content{
        engine = create_engine(f'mysql://{config("DB_USER")}:{quote_plus(config("DB_PASSWORD"))}@{config("DB_CONNECTION")}/{config("DB_NAME")}')
        conn = engine.connect()
        Base = declarative_base()
        Session = sessionmaker(bind=engine)
        session = Session()

        }
    })


Variable syntax
----------------

 .. code-block:: html
    
   {{choices.database}}

    ==
    {{name}}

    ==
    {{name|ucfirst}}
    ==
    {{name|replace(e,1)}}
    ==
    {{name|if(dev,1)}}
 