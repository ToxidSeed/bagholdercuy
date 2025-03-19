from model.seriemensual import SerieMensualModel
from app import db
from sqlalchemy.sql import func

class SerieMensualReader:

    @staticmethod
    def get_estadisticas(cod_symbol):
        stmt = db.select(
            func.max(SerieMensualModel.fch_ini_mes).label("max_fch_mes"),
            func.min(SerieMensualModel.fch_ini_mes).label("min_fch_mes"),
            func.count(1).label("cantidad")
        ).where(
            SerieMensualModel.symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        records = result.first()
        return records

    def get_series_desde_fecha(symbol, fch_mes=None):

        stmt = db.select(
            SerieMensualModel
        ).where(
            SerieMensualModel.symbol == symbol
        )

        if fch_mes is not None:
            stmt = stmt.where(SerieMensualModel.fch_ini_mes >= fch_mes)

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    def get_serie(symbol, fch_ini_mes):

        stmt = db.select(
            SerieMensualModel
        ).where(
            SerieMensualModel.symbol == symbol,
            SerieMensualModel.fch_ini_mes == fch_ini_mes
        )

        result = db.session.execute(stmt)
        records = result.scalars().first()
        return records


