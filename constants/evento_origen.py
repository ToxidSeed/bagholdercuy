from typing import NamedTuple
from . import register_init

_evento_origen = None

class EventoOrigen:
    __slots__ = ("_map",)

    def __init__(self, rows):
        self._map = {r.cod_evento: r for r in rows}

    def get(self, name: str):
        try:
            return self._map[name]
        except KeyError:
            raise KeyError(f"EventoOrigen.{name} no existe")


@register_init("evento_origen")
def init_evento_origen():
    global _evento_origen
    from reader.evento_origen import EventoOrigenReader

    rows = EventoOrigenReader.get_list()
    _evento_origen = EventoOrigen(rows)
    return _evento_origen


def get_evento_origen():
    if _evento_origen is None:
        return init_evento_origen()
    return _evento_origen


def __getattr__(name):
    if name == "evento_origen":
        return get_evento_origen()
    raise AttributeError(f"module has no attribute {name}")
