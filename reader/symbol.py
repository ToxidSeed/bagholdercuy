from model.StockSymbol import StockSymbol
from common.AppException import AppException

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

    def get_list():
        stmt = db.select(
            StockSymbol
        ).order_by(
            StockSymbol.symbol.asc()
        )

        results = db.session.execute(stmt)
        return results.scalars().all()