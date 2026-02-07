from parser.base import BaseParser

class VariacionSemanalParser:
    def parse_args_get_variacion_actual(self, args={}):
        params = {}
        parser = BaseParser(args=args)
        params["cod_symbol"] = parser.get("cod_symbol", requerido=True)
        return params

    def parse_args_get_variacion_semana_actual(self, args=None):
        params = {}
        parser = BaseParser(args=args)
        params["cod_symbol"] = parser.get(nombre_param="cod_symbol", requerido=True)
        params["cod_semana"] = parser.get(nombre_param="cod_semana", requerido=True, datatype=int)
        return params
