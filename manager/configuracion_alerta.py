from model.configuracionalerta import ConfiguracionAlertaModel
from reader.configuracionalerta import ConfiguracionAlertaReader
from reader.symbol import SymbolReader
from common.AppException import AppException
from collections import namedtuple
from app import db
from dataclasses import dataclass

@dataclass
class DatosActualizar:
    id_config_alerta: None
    cod_tipo_variacion_imp_accion: None
    ctd_variacion_imp_accion: None
    ctd_ciclos: None
    imp_inicial_ciclos: None

class ConfiguracionAlertaManager:

    def registrar(self, nueva_configuracion_alerta: ConfiguracionAlertaModel):
        configuracion_alerta_reader = ConfiguracionAlertaReader()
        symbol_reader = SymbolReader()

        id_symbol = nueva_configuracion_alerta.id_symbol
        id_cuenta = nueva_configuracion_alerta.id_cuenta

        # validando la cuenta
        symbol = symbol_reader.get(id_symbol=id_symbol)
        if symbol is None:
            raise AppException(msg=f"No se encuentra el symbol con id {id_symbol}")

        # validando la existencia de la configuracion
        configuracion_alerta = configuracion_alerta_reader.get_key2(id_cuenta=id_cuenta, id_symbol=id_symbol)
        if configuracion_alerta is not None:
            raise AppException(msg=f"ya se encuentra una alerta registrada para la cuenta {id_cuenta} y el symbol {symbol.symbol}")

        db.session.add(nueva_configuracion_alerta)
        return nueva_configuracion_alerta

    def actualizar(self, datos_actualizar: DatosActualizar):
        configuracion_alerta_reader = ConfiguracionAlertaReader()
        configuracion_alerta = configuracion_alerta_reader.get(id_config_alerta=datos_actualizar.id_config_alerta)
        if configuracion_alerta is None:
            raise AppException(msg=f"No se encuentra la configuracion con id: {datos_actualizar.id_config_alerta}")

        configuracion_alerta.cod_tipo_variacion_imp_accion = datos_actualizar.cod_tipo_variacion_imp_accion
        configuracion_alerta.ctd_variacion_imp_accion = datos_actualizar.ctd_variacion_imp_accion
        configuracion_alerta.ctd_ciclos = datos_actualizar.ctd_ciclos
        configuracion_alerta.imp_inicial_ciclos = datos_actualizar.imp_inicial_ciclos

        return configuracion_alerta





