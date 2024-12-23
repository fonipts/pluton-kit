============
Command line
============

plutonkit Default CLI
-----------------------
In starting your journey, you should start exploring our cli option


.. code-block:: bash

    plutonkit [OPTIONS]

options
-------

.. option:: clone_project
.. rubric:: Clone your project from project.yaml file
:arguments: source=[location of project.yaml]

.. option:: create_achitecture
.. rubric:: Create your first architecture
:arguments: <command>


.. option:: create_project
.. rubric:: Start creating your project in our listed framework
:arguments: source=[location of architecture.yaml]


.. option:: cmd
.. rubric:: Executing command using plutonkit
:arguments: <command>


.. option:: validate_blueprint
.. rubric:: Check your blueprint before issue before deploying
:arguments: [location of architecture.yaml]


In using `cmd` argument
------------------------
Below is sample for command you can use at your `command.yaml`
-   

    In our build `cmd` command given the name was `name`

    ::

        plutonkit cmd name

    Or short command using `plkcmd`

    ::

        plkcmd name
