from controller.base import Base
from common.Response import Response
from common.AppException import AppException
from reader.stocksplit import StockSplitReader
from service.stocksplit import StockSplitFMPService
from config.extensions import db

class StockSplitController(Base):
    def get_all_aplits(self, args={}):
        try:
            records = StockSplitReader.get_all_splits()
            return Response().from_raw_data(records)                        
        except Exception as e:            
            return Response().from_exception(e)

    def load_stock_splits(self, args={}):
        try:
            cod_symbol = args.get("cod_symbol")
            ss_service = StockSplitFMPService()
            ss_service.procesar(cod_symbol=cod_symbol)
            db.session.commit()
            return Response(msg="Se ha registrado correctamente")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

class FmpStockSplitController(StockSplitController):
    def load_stock_splits(self, args={}):
        try:
            print(args)
            cod_symbol = args.get("cod_symbol")
            ss_service = StockSplitFMPService()
            ss_service.procesar(cod_symbol=cod_symbol)
            db.session.commit()
            return Response(msg="Se ha registrado correctamente")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)
