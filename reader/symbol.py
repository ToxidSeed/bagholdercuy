from model.StockSymbol import StockSymbol
from common.AppException import AppException
from config.general import DEFAULT_LIMIT

from app import db

class SymbolReader:

    def get(cod_symbol=None, id_symbol=None):
        if cod_symbol is None and id_symbol is None:
            raise AppException(msg="No se ha indicado el codigo o el id del symbol")

        stmt = db.select(
            StockSymbol    
        )

        if cod_symbol is not None:
            stmt = stmt.where(
                StockSymbol.symbol == cod_symbol
            )
            result = db.session.execute(stmt)
            return result.scalars().first()
        
        if id_symbol is not None:
            stmt = stmt.where(
                StockSymbol.id == id_symbol
            )

        result = db.session.execute(stmt)
        return result.scalars().first()

    def get_list(args={}):
        id_symbol = args["id_symbol"]

        stmt = db.select(
            StockSymbol
        )
        
        if id_symbol is not None:
            stmt = stmt.where(
                StockSymbol.id == id_symbol
            )

        stmt = stmt.order_by(
            StockSymbol.symbol.asc()
        )

        stmt = stmt.limit(DEFAULT_LIMIT)

        results = db.session.execute(stmt)
        return results.scalars().all()