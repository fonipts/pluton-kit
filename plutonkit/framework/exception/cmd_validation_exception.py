class CmdValidationException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        self.message = message
        super().__init__(message)
