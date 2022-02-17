class AppException(Exception):
    def __init__(self, msg="", errors=[], extra=None):
        self.msg = msg
        self.errors = errors
        self.extra = extra        
    