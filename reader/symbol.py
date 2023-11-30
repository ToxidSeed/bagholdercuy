from model.StockSymbol import StockSymbol
from common.AppException import AppException
from config.general import DEFAULT_LIMIT

from app import db

class SymbolReader:
    def __init__(self, buffer=False):
        self.__buffer = buffer
        self.__memoria = {},        

    def get(self, cod_symbol=None, id_symbol=None, not_found_error=False) -> StockSymbol:        

        if cod_symbol is None and id_symbol is None:
            raise AppException(msg="No se ha indicado el codigo o el id del symbol")

        if cod_symbol is not None:
            return self.__get_x_cod_symbol(cod_symbol=cod_symbol, not_found_error=not_found_error)    
        
        if id_symbol is not None:
            return self.__get_x_id(id_symbol=id_symbol, not_found_error=not_found_error)

        return None        
    
    def __get_x_cod_symbol(self, cod_symbol, not_found_error=False):
        if self.__buffer is True:
            symbol = self.__memoria.get(cod_symbol)
            if symbol is not None:
                return symbol
            
        query = db.select(
            StockSymbol    
        ).where(
            StockSymbol.symbol == cod_symbol
        )

        result = db.session.execute(query)
        record = result.scalars().first()

        if record is None and not_found_error is True:            
            raise AppException(msg=f"No se ha encontrado symbol para {cod_symbol}")

        if record is not None and self.__buffer is True:
            self.__memoria[cod_symbol] = record
        
        return record

    def __get_x_id(self, id_symbol, not_found_error=False):
        if self.__buffer is True:
            symbol = self.__memoria.get(id_symbol)
            if symbol is not None:
                return symbol
            
        query = db.select(
            StockSymbol    
        ).where(
            StockSymbol.id == id_symbol
        )

        result = db.session.execute(query)
        record = result.scalars().first()

        if record is None and not_found_error is True:
            raise AppException(msg=f"No se ha encontrado symbol para el id: {id_symbol}")
        
        if record is not None and self.__buffer is True:
            self.__memoria[id_symbol] = record
        
        return record

    def get_list(args={}):
        id_symbol = args["id_symbol"]
        cod_symbol = args.get("cod_symbol")

        stmt = db.select(
            StockSymbol
        )
        
        if id_symbol is not None:
            stmt = stmt.where(
                StockSymbol.id == id_symbol
            )

        if cod_symbol is not None:
            stmt = stmt.where(
                StockSymbol.symbol == cod_symbol
            )

        stmt = stmt.order_by(
            StockSymbol.symbol.asc()
        )

        stmt = stmt.limit(DEFAULT_LIMIT)

        results = db.session.execute(stmt)
        return results.scalars().all()