from model.stocksplit import StockSplitModel

from app import db

class StockSplitReader:

    @staticmethod
    def get_splits(cod_symbol, recientes_primero=True):
        stmt = db.select(
            StockSplitModel
        ).where(
            StockSplitModel.cod_symbol == cod_symbol
        )

        if recientes_primero:
            stmt.order_by(
                StockSplitModel.fch_split.desc()
            )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    @staticmethod
    def get_all_splits(id_symbol=None):
        stmt = db.select(
            StockSplitModel
        )

        if id_symbol is not None:
            stmt.where(
                StockSplitModel.id_symbol == id_symbol
            )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records
