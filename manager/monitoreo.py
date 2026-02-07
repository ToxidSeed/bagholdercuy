from model.configuracionalerta import ConfiguracionAlertaModel
from model.monitoreo import MonitoreoModel
from reader.monitoreo import MonitoreoReader
from reader.symbol import SymbolReader

from app import db
from datetime import date
from common.AppException import AppException


class MonitoreoManager:

    def registrar(self, monitoreo_nuevo: MonitoreoModel) -> MonitoreoModel:
        monitoreo_reader = MonitoreoReader()
        symbol_reader = SymbolReader()

        symbol = symbol_reader.get(id_symbol=monitoreo_nuevo.id_symbol)
        if symbol is None:
            raise AppException(msg=f"No se ha encontrado un symbol con id {monitoreo_nuevo.id_symbol}")

        monitoreo = monitoreo_reader.get_key1(id_symbol=monitoreo_nuevo.id_symbol, id_cuenta=monitoreo_nuevo.id_cuenta)
        if monitoreo is not None:
            raise AppException(
                f"El monitoreo con symbol {symbol.symbol} y id cuenta {monitoreo_nuevo.id_cuenta} ya existe en la base de datos")

        db.session.add(monitoreo_nuevo)
        return monitoreo_nuevo
