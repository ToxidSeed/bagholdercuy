from . import register_init

_tipo_transaccion = None


class TipoTransaccion:
    __slots__ = ("_map",)

    def __init__(self, rows):
        self._map = {r.cod_tipo_transaccion: r.id_tipo_transaccion for r in rows}

    def __getattr__(self, name: str):
        try:
            return self._map[name]
        except KeyError:
            raise AttributeError(f"TipoTransaccion.{name} no existe")


@register_init("tipo_transaccion")
def init_tipo_transaccion():
    global _tipo_transaccion
    from reader.tipo_transaccion import TipoTransaccionReader

    rows = TipoTransaccionReader.get_list()
    _tipo_transaccion = TipoTransaccion(rows)
    return _tipo_transaccion


def get_tipo_transaccion():
    if _tipo_transaccion is None:
        return init_tipo_transaccion()
    return _tipo_transaccion

            
