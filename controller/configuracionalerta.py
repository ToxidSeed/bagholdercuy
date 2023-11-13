from controller.base import Base
from parser.configuracionalerta import ConfiguracionAlertaParser
from common.AppException import AppException
from common.Response import Response
from app import db

class ConfiguracionAlertaController(Base):
    def __init__(self):
        pass

    def registrar(self, args={}):
        try:
            parser = ConfiguracionAlertaParser()
            configuracion_alerta = parser.parse_args_registrar(args=args)
            db.session.add(configuracion_alerta)
            db.session.commit()
            return Response(msg="Se ha registrado la configuracion de la alerta de forma correcta")
        except Exception as e:
            db.session.rollback()
            raise AppException(msg=f"Ocurrio un error al registrar la configuracion para las alertas {str(e)}")