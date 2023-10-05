from app import db

from sqlalchemy import delete

from model.StockSymbol import StockSymbol

class SymbolRemover:
    def eliminar_todo():
        stmt = (
            delete(StockSymbol)
        )

        db.session.execute(stmt)