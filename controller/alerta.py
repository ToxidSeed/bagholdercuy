from controller.base import Base
from parser.alerta import AlertaParser
from reader.alerta import AlertaReader
from common.Response import Response


class AlertaController(Base):
    def get_list(self, args={}):
        pass

    def get_alertas_x_configuracion(self, args=None):
        if args is None:
            args = {}

        alerta_parser = AlertaParser()
        alerta_reader = AlertaReader()

        args = alerta_parser.parse_args_get_alertas_x_configuracion(args=args)
        id_config_alerta = args["id_config_alerta"]

        records = alerta_reader.get_alertas_x_configuracion(id_config_alerta=id_config_alerta)
        return Response().from_raw_data(records)

