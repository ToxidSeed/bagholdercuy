from parser.base import BaseParser

class SymbolFinderParser:
    def parse_args_get_list(args={}):
        id_symbol = BaseParser.parse_int(args.get("id_symbol"))
        args["id_symbol"] = id_symbol
        return args
        