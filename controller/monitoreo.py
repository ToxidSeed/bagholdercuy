from controller.base import Base
from parser.monitoreo import MonitoreoParser
from reader.monitoreo import MonitoreoReader
from common.Response import Response

class MonitoreoController(Base):

    def get_monitoreo_activo(self, args={}):
        monitoreo_parser = MonitoreoParser()
        monitoreo_reader = MonitoreoReader()

        args = monitoreo_parser.parse_args_get_lista_seguimiento(args=args)
        records = monitoreo_reader.get_monitoreo_activo(id_cuenta=args.get("id_cuenta"))
        return Response().from_raw_data(records)