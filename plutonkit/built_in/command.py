import sys

class PLCommand:
    def __init__(self):
        self.local_cli = {}

    def cli(self,name = None):
        def cli_real_decorator(function):
            
            def wrapper(*args,**kwargs):

                return function(*args,**kwargs)
            self.local_cli[name] = {"func":function}
            return wrapper
        return cli_real_decorator    
    
    def run(self):
        print(sys.argv,"::")
        self.local_cli["test"]["func"](13,2)