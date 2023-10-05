from model.StockSymbol import StockSymbol

from app import db

class SymbolReader:

    def get(symbol):
        symbol = StockSymbol.query.filter(
            StockSymbol.symbol == symbol
        ).first()

        return symbol

    def get_list():
        stmt = db.select(
            StockSymbol
        ).order_by(
            StockSymbol.symbol.asc()
        )

        results = db.session.execute(stmt)
        return results.scalars().all()