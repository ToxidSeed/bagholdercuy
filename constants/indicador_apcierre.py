from . import register_init

_indicador_apcierre = None


class IndicadorApcierre:
    __slots__ = ("_map",)

    def __init__(self, rows):
        self._map = {r.cod_indicador: r for r in rows}

    def get(self, name: str):
        try:
            return self._map[name]
        except KeyError:
            raise KeyError(f"IndicadorApcierre.{name} no existe")

    @property
    def APERTURA(self):
        return self.get("O")

    @property
    def CIERRE(self):
        return self.get("C")


@register_init("indicador_apcierre")
def init_indicador_apcierre():
    global _indicador_apcierre
    from reader.indicador_apcierre import IndicadorApcierreReader

    rows = IndicadorApcierreReader.get_list()
    _indicador_apcierre = IndicadorApcierre(rows)
    return _indicador_apcierre


def get_indicador_apcierre():
    if _indicador_apcierre is None:
        return init_indicador_apcierre()
    return _indicador_apcierre


def __getattr__(name):
    if name == "indicador_apcierre":
        return get_indicador_apcierre()
    raise AttributeError(f"module has no attribute {name}")

