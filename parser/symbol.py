from parser.base import BaseParser

class SymbolFinderParser:

    @staticmethod
    def parse_args_get_list(args={}):
        parser = BaseParser(args=args)
        id_symbol = parser.get("id_symbol", datatype=int, vacio_es_nulo=True)                
        args["id_symbol"] = id_symbol

        cod_symbol = parser.get("cod_symbol", vacio_es_nulo=True)        
        args["cod_symbol"] = cod_symbol
        
        return args
        