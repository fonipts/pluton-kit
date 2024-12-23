============
Overview
============



Project file and folder design concept
--------------------------------------

In file ``architecture.yaml``

 .. code-block:: yaml


   name: bottle
    settings:
        install_type: pip
    choices:
    - name: name
        question: What is your name
        type: input
    - name: database
        question: What is your Database choice?
        type: single_choice
        option:
        - postgres
        - mysql
        - none
    - name: redis
        question: Do you want Redis?
        type: single_choice
        option:
        - "yes"
        - "no"
    script:
        pip_install:
            description: Install package
            command:
            - pip install -r requirements.txt
        start:
            command:
            - python main.py
    files:
        default:
            - file: main.tplpy
            - file: README.md
        optional:
            - condition: database != "none"
            dependent:
            - file: db.tplpy
            - file: .env
            - condition: docker != "No plan"
            dependent:
            - file: Dockerfile.tpl

    bootscript:
    - command: pip install -r requirements.txt
        exec_position: start
