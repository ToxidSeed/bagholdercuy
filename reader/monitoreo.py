from app import db
from model.monitoreo import MonitoreoModel
from model.StockSymbol import StockSymbol as StockSymbolModel
from common.AppException import AppException
from sqlalchemy.orm import join

class MonitoreoReader:
    def get(self, id_monitoreo):
        query = db.select(
            MonitoreoModel
        ).where(
            MonitoreoModel.id_monitoreo == id_monitoreo
        )

        result = db.session.execute(query)
        return result.scalars().first()
    
    def get_unique1(self, id_symbol, id_cuenta, error_si_no_existe=False):
        query = db.select(
            MonitoreoModel
        ).where(
            MonitoreoModel.id_symbol == id_symbol,
            MonitoreoModel.id_cuenta == id_cuenta
        )

        result = db.session.execute(query)
        record = result.scalars().first()
        if record is None and error_si_no_existe is True:
            raise AppException(msg=f"No existe el monitoreo para el id symbol {id_symbol} y el id cuenta {id_cuenta}")
        
        return record
    
    def get_monitoreo_activo(self, id_cuenta):
        query = db.select(
            MonitoreoModel.id_monitoreo,
            MonitoreoModel.id_symbol,
            MonitoreoModel.id_cuenta,
            MonitoreoModel.fch_registro,
            StockSymbolModel.symbol.label("cod_symbol"),
            StockSymbolModel.name.label("nom_symbol")
        ).select_from(
            MonitoreoModel
        ).join(
            StockSymbolModel, MonitoreoModel.id_symbol == StockSymbolModel.id
        ).where(
            MonitoreoModel.id_cuenta == id_cuenta
        )

        result = db.session.execute(query)
        records = result.all()
        return records


