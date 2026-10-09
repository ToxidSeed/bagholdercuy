from . import register_init

_symbol_type = None

"""
cod_symbol_type
STOCK
OPTION
BOND
ETF
FUTURE
"""


class SymbolType:
    __slots__ = ("_map",)

    def __init__(self, rows):
        self._map = {r.cod_symbol_type: r.id_symbol_type for r in rows}

    def __getattr__(self, name: str):
        try:
            return self._map[name]
        except KeyError:
            raise AttributeError(f"SymbolType.{name} no existe")


@register_init("symbol_type")
def init_symbol_type():
    global _symbol_type
    from reader.symbol_type import SymbolTypeReader

    rows = SymbolTypeReader.get_list()
    _symbol_type = SymbolType(rows)
    return _symbol_type


def get_symbol_type():
    if _symbol_type is None:
        return init_symbol_type()
    return _symbol_type
