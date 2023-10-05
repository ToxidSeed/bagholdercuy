from model.seriemensual import SerieMensualModel
from app import db

class SerieMensualReader:
    
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


