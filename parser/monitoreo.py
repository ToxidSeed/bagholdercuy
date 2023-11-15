from parser.base import BaseParser

class MonitoreoParser:
    def parse_args_get_lista_seguimiento(self, args={}):
        parser = BaseParser(args=args)
        args["id_cuenta"] = parser.get("id_cuenta", requerido=True, datatype=int)
        return args
