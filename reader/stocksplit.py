from model.stocksplit import StockSplitModel

from config.extensions import db

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
        else:
            stmt.order_by(
                StockSplitModel.fch_split.asc()
            )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    @staticmethod
    def get_all_splits(id_symbol=None, cod_symbol=None):
        stmt = db.select(
            StockSplitModel
        )

        if id_symbol is not None:
            stmt.where(
                StockSplitModel.id_symbol == id_symbol
            )

        if cod_symbol is not None:
            stmt.where(
                StockSplitModel.cod_symbol == cod_symbol
            )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    @staticmethod
    def get_factor_split_acum(cod_symbol, fch_split):
        stmt = db.select(
            StockSplitModel
        ).where(
            StockSplitModel.cod_symbol == cod_symbol,
            StockSplitModel.fch_split >= fch_split
        )

        result = db.session.execute(stmt)
        records = result.scalars().all()

        factor_split_acum = 1
        for split in records:
            factor_split_acum = factor_split_acum * float(split.factor_split)
        
        return (factor_split_acum, records)

    @staticmethod
    def get_split_por_fecha(cod_symbol, fch_ref):
        stmt = db.select(
            StockSplitModel
        ).where(
            StockSplitModel.cod_symbol == cod_symbol,
            StockSplitModel.fch_split > fch_ref,
            StockSplitModel.fch_split_anterior <= fch_ref
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()
        return record



