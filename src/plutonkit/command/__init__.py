
from plutonkit.config import INTRODUCTION
from plutonkit.config.system import SERVICE_TYPE
from plutonkit.core.helper.command import callback_execute

def autoload():

    DETAILS_COMMAND = {
        "details":{},
        "command":[]
    }

    TEMPLATE = "%s" % (INTRODUCTION)
    print(TEMPLATE)

    callback_execute(DETAILS_COMMAND,"What is your service type?",SERVICE_TYPE)
