class BaseParser:
    def __init__(args={}):
        self.args = args

    def get_arg(self, arg=""):
        if arg in self.args:
            raise AppException(msg="No se ha enviado {0}".format(arg))
        return arg
