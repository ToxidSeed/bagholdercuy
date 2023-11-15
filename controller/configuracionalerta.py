from controller.base import Base
from parser.configuracionalerta import ConfiguracionAlertaParser
from common.AppException import AppException
from common.Response import Response
from manager.alerta import AlertaManager
from manager.monitoreo import MonitoreoManager
from model.configuracionalerta import ConfiguracionAlertaModel
from reader.configuracionalerta import ConfiguracionAlertaReader
from datetime import date

from app import db

class ConfiguracionAlertaController(Base):
    def __init__(self):
        pass

    def registrar(self, args={}):
        try:
            parser = ConfiguracionAlertaParser()
            alerta_manager = AlertaManager()
            
            
            #transformarmos los argumentos a objeto
            configuracion_alerta = parser.parse_args_registrar(args=args)

            #primero se guarda el monitoreo del symbol
            self.registrar_monitoreo_si_no_enviado(configuracion_alerta=configuracion_alerta)

            #guardamos la configuracion de la alerta
            db.session.add(configuracion_alerta)
            db.session.flush()

            #generamos las alertas
            alerta_manager.generar(configuracion_alerta=configuracion_alerta)
            db.session.commit()
            return Response(msg="Se ha registrado la configuracion de la alerta de forma correcta")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)
        
    def registrar_monitoreo_si_no_enviado(self, configuracion_alerta:ConfiguracionAlertaModel):
        monitoreo_manager = MonitoreoManager()

        if configuracion_alerta.id_monitoreo is None:
            #registrar
            monitoreo = monitoreo_manager.registrar_desde_configuracion_alerta(configuracion_alerta)
            db.session.flush()
            configuracion_alerta.id_monitoreo = monitoreo.id_monitoreo       
            return monitoreo
        
    def get_configuracion_alerta(self, args={}):
        args = ConfiguracionAlertaParser().parse_args_get_configuracion_alerta(args=args)
        id_monitoreo = args.get("id_monitoreo")

        configuracion_alerta_reader = ConfiguracionAlertaReader()
        configuracion_alerta = configuracion_alerta_reader.get_key1(id_monitoreo=id_monitoreo)
        return Response().from_raw_data(configuracion_alerta)

        
