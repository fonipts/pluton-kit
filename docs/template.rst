============
Template
============
The goal is to have an idea in building function in template and reuse to if you import to different project.

Most of pass value are coming from `choices` and `env` at ``architecture.yaml``


Filename format
----------------
------------------------
Template extension name
------------------------
This function syntax will work on *.tpl{ext file} format otherwise it will be ignore in execution.
-   

    Given your filename was format like this

    ::

        helloworld.tplpy

    After executing the following format will be modified to:

    ::

        helloworld.py

----------------------------------
Using variable format in filename
----------------------------------
To allowed using variable modification to rename your expected name to your preference

-   

    Given your ``filename`` was value to ``helloworld``

    ::

        {{filename}}.tplpy

    After executing the following format will be modified to:

    ::

        helloworld.py

Functional syntax
------------------
This feature was offered, to support the concept 

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

.. list-table:: Syntax or function that is available in template
   :widths: 25 25 50
   :header-rows: 1

   * - Action name
     - Description
     - Example
   * - end
     - End of statement 
     - @end{ }
   * - condition
     - creating your conditional statement	
     - @condition{ database == "postgres" }
   * - content
     - Content of template function that you want to render	
     - @content{ Hi }
   * - load
     - If use *.tpl{file extension} then it will render the template function or else render of the text content	 
     - @load{ ./tests/raw/tpl/test_temp.tplpy }
   * - script
     - Execute python script in your template, please note ``content`` was used to render the output string in template
     - @script{ content ="Hi" }      

Variable syntax
----------------


In this example we are replacing some value given in your choices and env to replace

-   

    Given your ``name`` was value to ``helloworld``

    ::

        {{name}}

        ==
        {{name|ucfirst}}
        ==
        {{name|replace(e,1)}}
        ==
        {{name|if(helloworld,1)}}

    After executing the following format will be modified to:

    ::

        helloworld

        ==
        Helloworld
        ==
        H1lloworld
        ==
        1


.. list-table:: Action you can use in variable syntax
   :widths: 25 25 50
   :header-rows: 1

   * - Action name
     - Description
     - Example
   * - ucfirst
     - Upper case first string	
     - {{name|ucfirst}}
   * - lower
     - Lower case string
     - {{name|lower}}
   * - upper
     - Upper case string	
     - {{name|upper}}
   * - replace
     - Replace string
     - {{name|replace(e,1)}}
   * - if
     - If statement string	
     - {{name|if(dev,1)}}
 