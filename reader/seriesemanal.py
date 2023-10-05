from model.seriesemanal import SerieSemanalModel
from app import db

class SerieSemanalReader:

    def get_series_desde_fecha(symbol, fch_semana=None):
        
        stmt = db.select(
            SerieSemanalModel
        ).where(
            SerieSemanalModel.symbol == symbol
        )

        if fch_semana is not None:
            stmt = stmt.where(
                SerieSemanalModel.fch_semana >= fch_semana
            )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    def get_serie(symbol, fch_semana):

        stmt = db.select(
            SerieSemanalModel
        ).where(
            SerieSemanalModel.symbol == symbol,
            SerieSemanalModel.fch_semana == fch_semana
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()
        return record