from . import register_init

_instrumento_financiero = None

"""
cod_instrumento_financiero
STOCK
OPTION
BOND
ETF
FUTURE
"""

class InstrumentoFinanciero:
    __slots__ = ("_map",)

    def __init__(self, rows):
        self._map = {r.cod_instrumento_financiero: r.id_instrumento_financiero for r in rows}

    def __getattr__(self, name: str):
        try:
            return self._map[name]
        except KeyError:
            raise AttributeError(f"InstrumentoFinanciero.{name} no existe")


@register_init("instrumento_financiero")
def init_instrumento_financiero():
    global _instrumento_financiero
    from reader.instrumento_financiero import InstrumentoFinancieroReader

    rows = InstrumentoFinancieroReader.get_list()
    _instrumento_financiero = InstrumentoFinanciero(rows)
    return _instrumento_financiero


def get_instrumento_financiero():
    if _instrumento_financiero is None:
        return init_instrumento_financiero()
    return _instrumento_financiero
