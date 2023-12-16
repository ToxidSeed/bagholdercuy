from parser.base import BaseParser
from collections import namedtuple

class SymbolParser:

    def parse_args_get_symbol_x_codigo(self, args={}):
        parser = BaseParser(args=args)
        cod_symbol = parser.get("cod_symbol", requerido=True)
        args["cod_symbol"] = cod_symbol
        return args

class SymbolFinderParser:

    @staticmethod
    def parse_args_get_list(args={}):
        parser = BaseParser(args=args)
        id_symbol = parser.get("id_symbol", datatype=int, vacio_es_nulo=True)                
        args["id_symbol"] = id_symbol

        cod_symbol = parser.get("cod_symbol", vacio_es_nulo=True)        
        args["cod_symbol"] = cod_symbol
        
        return args

    def parse_args_get(self, args={}):
        params = namedtuple("params", ["id_symbol"])

        parser = BaseParser(args=args)
        id_symbol = parser.get("id_symbol", datatype=int, vacio_es_nulo=True)
        params = params(id_symbol=id_symbol)

        return params