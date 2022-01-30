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

def is_error(object=None):
    if object is None:
        return False
    if type(object) is Error:
        return True
        