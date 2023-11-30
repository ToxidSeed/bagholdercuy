from controller.base import Base
from parser.monitoreo import MonitoreoParser
from reader.monitoreo import MonitoreoReader
from common.Response import Response
from manager.monitoreo import MonitoreoManager
from app import db

class MonitoreoController(Base):

    def get_monitoreo_activo(self, args={}):
        monitoreo_parser = MonitoreoParser()
        monitoreo_reader = MonitoreoReader()

        requeridos, opcionales = monitoreo_parser.parse_args_get_lista_seguimiento(args=args)
        records = monitoreo_reader.get_monitoreo_activo(id_cuenta=requeridos.get("id_cuenta"), opcionales=opcionales)
        return Response().from_raw_data(records)

    def registrar(self, args={}):
        try:
            monitoreo_parser = MonitoreoParser()

            monitoreo_nuevo = monitoreo_parser.parse_args_registrar(args=args)
            MonitoreoManager().registrar(monitoreo_nuevo=monitoreo_nuevo)

            db.session.commit()
            return Response(msg="Se ha registrado el monitoreo correctamente")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)
