"""Module providing a function printing python version."""

def format_argument(type,name,question,option_name,config):
    return {
        "field_type":"input",
        "type":type,
        "name":name,
        "option_name":option_name,
        "question":question,
        "config":config
    }

