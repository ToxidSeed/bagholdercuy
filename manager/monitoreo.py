from model.configuracionalerta import ConfiguracionAlertaModel
from model.monitoreo import MonitoreoModel
from reader.monitoreo import MonitoreoReader
from app import db
from datetime import date
from common.AppException import AppException

class MonitoreoManager:
    def guardar(self):
        pass

    def registrar(self, monitoreo:MonitoreoModel):
        pass

    def registrar_desde_configuracion_alerta(self, configuracion_alerta:ConfiguracionAlertaModel):        
        monitoreo_reader = MonitoreoReader()

        monitore_existente = monitoreo_reader.get_unique1(id_symbol=configuracion_alerta.id_symbol, id_cuenta=configuracion_alerta.id_cuenta)
        if monitore_existente is not None:
            raise AppException(f"El monitoreo con id symbol {configuracion_alerta.id_symbol} y id cuenta {configuracion_alerta.id_cuenta} ya existe en la base de datos")

        monitoreo = MonitoreoModel(
            id_cuenta = configuracion_alerta.id_cuenta,
            id_symbol = configuracion_alerta.id_symbol,
            fch_registro = date.today()
        )
        db.session.add(monitoreo)
        return monitoreo
            
            
    
    

    