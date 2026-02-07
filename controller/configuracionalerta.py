from controller.base import Base
from parser.configuracionalerta import ConfiguracionAlertaParser
from common.AppException import AppException
from common.Response import Response
from manager.alerta import AlertaManager
from manager.monitoreo import MonitoreoManager
from manager.configuracion_alerta import ConfiguracionAlertaManager
from model.configuracionalerta import ConfiguracionAlertaModel
from reader.configuracionalerta import ConfiguracionAlertaReader
from datetime import date

from app import db

class ConfiguracionAlertaController(Base):
    def __init__(self):
        pass

    def registrar(self, args=None):
        try:
            if args is None:
                args = {}

            parser = ConfiguracionAlertaParser()
            configuracion_alerta_manager = ConfiguracionAlertaManager()
            monitoreo_manager = MonitoreoManager()
            alerta_manager = AlertaManager()

            # transformarmos los argumentos a objeto
            configuracion_alerta, monitoreo = parser.parse_args_registrar(args=args)

            # primero se guarda el monitoreo del symbol
            monitoreo_manager.registrar(monitoreo_nuevo=monitoreo)
            db.session.flush()

            # guardamos la configuracion de la alerta
            configuracion_alerta.id_monitoreo = monitoreo.id_monitoreo
            configuracion_alerta_manager.registrar(nueva_configuracion_alerta=configuracion_alerta)
            db.session.flush()

            # generamos las alertas
            alerta_manager.generar(configuracion_alerta=configuracion_alerta)
            db.session.commit()
            return Response(msg="Se ha registrado la configuracion de la alerta de forma correcta")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def asociar_a_monitoreo(self, args=None):
        try:
            if args is None:
                args = {}

            parser = ConfiguracionAlertaParser()
            config_alerta_manager = ConfiguracionAlertaManager()
            alerta_manager = AlertaManager()

            configuracion_alerta = parser.parse_args_asociar_a_monitoreo(args=args)
            config_alerta_manager.registrar(nueva_configuracion_alerta=configuracion_alerta)
            db.session.flush()

            # generamos las alertas
            alerta_manager.generar(configuracion_alerta=configuracion_alerta)

            db.session.commit()
            return Response(msg="Se ha incluido correctamente en el monitoreo")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def actualizar(self, args=None):
        try:
            if args is None:
                args = {}

            parser = ConfiguracionAlertaParser()
            configuracion_alerta_manager = ConfiguracionAlertaManager()
            alerta_manager = AlertaManager()

            datos_actualizar = parser.parse_args_actualizar(args=args)

            # actualizamos los datos
            configuracion_alerta = configuracion_alerta_manager.actualizar(datos_actualizar=datos_actualizar)
            db.session.flush()

            # generamos las alertas
            alerta_manager.generar(configuracion_alerta=configuracion_alerta)

            db.session.commit()
            return Response(msg="Se ha actualizado la configuracion y generado las alertas para: ")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

        
    def get_configuracion_alerta(self, args={}):
        args = ConfiguracionAlertaParser().parse_args_get_configuracion_alerta(args=args)
        id_config_alerta = args.get("id_config_alerta")

        configuracion_alerta_reader = ConfiguracionAlertaReader()
        configuracion_alerta = configuracion_alerta_reader.get(id_config_alerta=id_config_alerta)
        return Response().from_raw_data(configuracion_alerta)




