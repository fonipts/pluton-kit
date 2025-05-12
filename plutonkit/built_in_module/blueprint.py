class PLBlueprint:
    def __init__(self):
        self.local_block = {}
        self.bootscript = []
        self.local_callback = {}

    def block(self,name = None):
        def block_real_decorator(function):

            def wrapper(*args,**kwargs):

                return function(*args,**kwargs)
            final_name = name is None and function.__name__ or name
            self.local_block[final_name] = {
              #  "description":description,
                "func":function
                }
            return wrapper
        return block_real_decorator

    def script(self,name = None):
        def script_real_decorator(function):

            def wrapper(*args,**kwargs):

                return function(*args,**kwargs)
            final_name = name is None and function.__name__ or name
            self.bootscript.append(
                {
                "name":final_name,
                "func":function
                }
            )
            return wrapper
        return script_real_decorator


    def get_execute(self):
        return {
            "block": self.local_block,
            "script": self.bootscript
        }
