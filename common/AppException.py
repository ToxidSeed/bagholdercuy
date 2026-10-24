class AppException(Exception):
    def __init__(self, msg="", errors=[], extra=None):
        super().__init__(msg)
        self.msg = msg
        self.errors = errors
        self.extra = extra

    def __str__(self):
        return self.msg        
    