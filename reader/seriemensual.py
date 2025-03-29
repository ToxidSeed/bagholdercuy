from model.seriemensual import SerieMensualModel
from app import db
from sqlalchemy.sql import func

class SerieMensualReader:

    @staticmethod
    def get_estadisticas(cod_symbol):
        stmt = db.select(
            func.max(SerieMensualModel.fch_mes).label("max_fch_mes"),
            func.min(SerieMensualModel.fch_mes).label("min_fch_mes"),
            func.count(1).label("cantidad")
        ).where(
            SerieMensualModel.cod_symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        records = result.first()
        return records

    def get_series_desde_fecha(symbol, fch_mes=None):

        stmt = db.select(
            SerieMensualModel
        ).where(
            SerieMensualModel.cod_symbol == symbol
        )

        if fch_mes is not None:
            stmt = stmt.where(SerieMensualModel.fch_mes >= fch_mes)

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    def get_serie(symbol, fch_ini_mes):

        stmt = db.select(
            SerieMensualModel
        ).where(
            SerieMensualModel.cod_symbol == symbol,
            SerieMensualModel.fch_mes == fch_ini_mes
        )

        result = db.session.execute(stmt)
        records = result.scalars().first()
        return records

    @staticmethod
    def get_max_fch_mes(cod_symbol):

        stmt = db.select(
            func.max(SerieMensualModel.fch_mes).label("fch_mes_max")
        ).where(
            SerieMensualModel.cod_symbol == cod_symbol,
        )

        result = db.session.execute(stmt)
        record = result.first()
        if record:
            return record.fch_mes_max

    @staticmethod
    def get_serie_anterior(cod_symbol, fch_serie_mensual):
        stmt = db.select(
            SerieMensualModel
        ).where(
            SerieMensualModel.cod_symbol == cod_symbol,
            SerieMensualModel.fch_mes < fch_serie_mensual
        ).order_by(
            SerieMensualModel.fch_mes.desc()
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()
        return record

