from parser.base import BaseParser
from model.monitoreo import MonitoreoModel


class MonitoreoParser:
    def parse_args_get_lista_seguimiento(self, args={}):
        parser = BaseParser(args=args)

        requeridos = {
            "id_cuenta": parser.get("id_cuenta", requerido=True, datatype=int)
        }

        opcionales = {}
        if "id_symbol" in args:
            opcionales["id_symbol"] = parser.get("id_symbol", datatype=int)

        return requeridos, opcionales

    def parse_args_registrar(self, args={}):
        parser = BaseParser(args=args)

        monitoreo = MonitoreoModel()
        monitoreo.id_symbol = parser.get("id_symbol", requerido=True, datatype=int)
        monitoreo.id_cuenta = parser.get("id_cuenta", requerido=True, datatype=int)
        return monitoreo
