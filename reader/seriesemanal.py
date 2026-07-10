from model.seriesemanal import SerieSemanalModel
from config.extensions import db
import sqlalchemy.sql.functions as func

class SerieSemanalReader:

    @staticmethod
    def get_estadisticas(cod_symbol):
        stmt = db.select(
            func.max(SerieSemanalModel.cod_semana).label("max_cod_semana"),
            func.min(SerieSemanalModel.cod_semana).label("min_cod_semana"),
            func.max(SerieSemanalModel.fch_semana).label("fch_semana_max"),
            func.min(SerieSemanalModel.fch_semana).label("fch_semana_min"),
            func.count(1).label("cantidad")
        ).where(
            SerieSemanalModel.symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        records = result.first()
        return records

    @staticmethod
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

    @staticmethod
    def get_max_fch_semana(cod_symbol):
        stmt = db.select(
            func.max(SerieSemanalModel.fch_semana).label("fch_semana")
        ).where(
            SerieSemanalModel.symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        record = result.first()
        if record:
            return record.fch_semana


    @staticmethod
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

    @staticmethod
    def get_fch_semana_previa(cod_symbol, fch_serie_semanal):
        stmt = db.select(
            func.max(SerieSemanalModel.fch_semana).label("fch_semana")
        ).where(
            SerieSemanalModel.symbol == cod_symbol,
            SerieSemanalModel.fch_semana < fch_serie_semanal
        )

        result = db.session.execute(stmt)
        fch_semana = result.scalars().first()
        return fch_semana

    @staticmethod
    def get_serie_anterior(symbol, fch_serie_semanal):
        stmt = db.select(
            SerieSemanalModel
        ).where(
            SerieSemanalModel.symbol == symbol,
            SerieSemanalModel.fch_semana < fch_serie_semanal
        ).order_by(
            SerieSemanalModel.fch_semana.desc()
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()
        return record

