class Error:
    def __init__(self, msg="", errors=[]):
        self.msg = msg
        self.errors = errors

    def add(self, msg=""):
        self.errors.append(msg)
    
    def has_errors(self):
        if len(self.errors) > 0:
            return True
        else:
            return False
        