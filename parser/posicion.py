from parser.base import BaseParser

class PosicionParser:
    def parse_args_get_posiciones_acciones(args={}):
        #id_cuenta
        id_cuenta = BaseParser.parse_int(args.get("id_cuenta"))
        args["id_cuenta"] = id_cuenta
        return args
    
    def parse_args_get_posiciones_contratos_opciones(args={}):
        #id_cuenta
        id_cuenta = BaseParser.parse_int(args.get("id_cuenta"))
        args["id_cuenta"] = id_cuenta
        return args
