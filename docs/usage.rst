============
Usage
============

Starting your first project template
------------------------

If do you not know where, then you can start by running this command in your terminal

 .. code-block:: shell


   plutonkit create_project

Then it will give you a selection of framework that you can start working in python(eventually we will add some supporting framework in other languages).

----------------------------------
Define your source of blueprint
----------------------------------

Given that you have a flavored path for that source blueprint/template. we suggest in using the code execution.

.. code-block:: shell


   plutonkit create_project source=https://github.com/fonipts/pluton-lobby.git/blueprint/ariadne

Given that you know the exact source path of your blueprint

or 

.. code-block:: shell


   plutonkit create_project name=ariadne

If you like our option at `pluton-lobby`

.. list-table:: Action you can use in variable syntax
   :widths: 25 75
   :header-rows: 1

   * - Project name
     - Description
   * - django
     - For django framework
   * - bottle
     - For bottle framework
   * - fastapi
     - For fastapi framework
   * - flask
     - For flask framework
   * - graphene
     - For graphene framework
   * - ariadne
     - For ariadne framework
   * - tartiflette
     - For tartiflette framework
   * - default_grpc
     - For default_grpc framework
   * - default_web3
     - For default_web3 framework
   * - default_starter_python
     - Your starter kit for Python language
   * - default_starter_golang
     - Your starter kit for Go language                         
   * - default_starter_ruby
     - Your starter kit for Ruby language 
   * - default_websocket
     - Your starkit websocket in python        
