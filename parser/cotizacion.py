from parser.base import BaseParser

class CotizacionParser:
    def parse_args_get_cotizacion(self, args={}):
        parser = BaseParser(args=args)
        args["cod_symbol"] = parser.get("cod_symbol", requerido=True)
        return args