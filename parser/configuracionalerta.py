from model.configuracionalerta import ConfiguracionAlertaModel
from model.monitoreo import MonitoreoModel
from parser.base import BaseParser
from common.AppException import AppException
from config.app_constants import TIPO_VARIACION_EJERCICIO

from reader.symbol import SymbolReader
from reader.monitoreo import MonitoreoReader
from reader.configuracionalerta import ConfiguracionAlertaReader

from manager.configuracion_alerta import ConfiguracionAlertaManager, DatosActualizar


from collections import namedtuple

class ConfiguracionAlertaParser:

    def parse_args_registrar(self, args={}):
        parser = BaseParser(args=args)
        
        configuracion = ConfiguracionAlertaModel()
        monitoreo = MonitoreoModel()

        configuracion.id_cuenta = parser.get("id_cuenta", datatype=int, requerido=True)
        configuracion.id_symbol = parser.get("id_symbol", requerido=True, datatype=int)
        configuracion.cod_tipo_variacion_imp_accion = parser.get("cod_tipo_variacion_imp_accion", requerido=True)
        configuracion.ctd_variacion_imp_accion = parser.get("ctd_variacion_imp_accion", requerido=True, datatype=int)
        configuracion.ctd_ciclos = parser.get("ctd_ciclos", requerido=True, datatype=int)
        configuracion.imp_inicial_ciclos = parser.get("imp_inicial_ciclos", requerido=True, datatype=float)

        monitoreo.id_cuenta = configuracion.id_cuenta
        monitoreo.id_symbol = configuracion.id_symbol

        monitoreo_existente = MonitoreoReader().get_key1(id_cuenta=monitoreo.id_cuenta, id_symbol=monitoreo.id_symbol)
        if monitoreo_existente is not None:
            raise AppException(msg=f"ya existe un monitoreo para la cuenta {configuracion.id_cuenta} y el symbol {configuracion.id_symbol}")

        return configuracion, monitoreo

    def parse_args_asociar_a_monitoreo(self, args={}):
        parser = BaseParser(args=args)

        configuracion = ConfiguracionAlertaModel()

        configuracion.id_monitoreo = parser.get("id_monitoreo", datatype=int, requerido=True)
        configuracion.id_symbol = parser.get("id_symbol", datatype=int, requerido=True)
        configuracion.id_cuenta = parser.get("id_cuenta", datatype=int, requerido=True)
        configuracion.imp_inicial_ciclos = parser.get("imp_inicial_ciclos", datatype=float, requerido=True)
        configuracion.ctd_ciclos = parser.get("ctd_ciclos", datatype=int, requerido=True)
        configuracion.ctd_variacion_imp_accion = parser.get("ctd_variacion_imp_accion", requerido=True, datatype=int)
        configuracion.cod_tipo_variacion_imp_accion = parser.get("cod_tipo_variacion_imp_accion", datatype=float, requerido=True)

        return configuracion

    def parse_args_actualizar(self, args=None):
        if args is None:
            args = {}

        parser = BaseParser(args=args)

        return DatosActualizar(
            id_config_alerta=parser.get("id_config_alerta", datatype=int, requerido=True),
            cod_tipo_variacion_imp_accion=parser.get("cod_tipo_variacion_imp_accion", requerido=True),
            ctd_variacion_imp_accion=parser.get("ctd_variacion_imp_accion", requerido=True, datatype=int),
            ctd_ciclos=parser.get("ctd_ciclos", requerido=True, datatype=int),
            imp_inicial_ciclos=parser.get("imp_inicial_ciclos", requerido=True, datatype=float)
        )

    def parse_args_get_configuracion_alerta(self, args={}):
        parser = BaseParser(args=args)
        id_config_alerta = parser.get("id_config_alerta",requerido=True, datatype=int)
        args["id_config_alerta"] = id_config_alerta
        return args

