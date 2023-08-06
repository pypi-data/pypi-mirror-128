class CLIError(Exception):
    """Base class for exceptions in this module."""
    pass

class ConnectionTimeOut(CLIError):
    """Exception raised when server closes connection due timeout"""

    def __init__(self, message='Server has closed the connection due time out'):
        super().__init__(message)

class CommandFailedError(CLIError):
    """Exception raised when server occures an error"""

    def __init__(self, message="Failed while executing the command"):
        super().__init__(message)
    
class NotValidCGPStringError(CLIError):
    """Exception raised when parser can't parse a string"""

    def __init__(self, message='Can not parse this string'):
        super().__init__(message)
    
class FailedLogin(CLIError):
    """Exception raised when username or password does not match"""

    def __init__(self, message='Wrong username or password'):
        super().__init__(message)