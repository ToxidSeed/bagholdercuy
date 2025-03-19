from model.seriesemanal import SerieSemanalModel
from app import db
import sqlalchemy.sql.functions as func

class SerieSemanalReader:

    @staticmethod
    def get_estadisticas(cod_symbol):
        stmt = db.select(
            func.max(SerieSemanalModel.cod_semana).label("max_cod_semana"),
            func.min(SerieSemanalModel.cod_semana).label("min_cod_semana"),
            func.count(1).label("cantidad")
        ).where(
            SerieSemanalModel.symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        records = result.first()
        return records

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