from model.variacionmensual import VariacionMensualModel
from app import db
from sqlalchemy.sql import func
import pandas as pd


class VariacionMensualReader:

    @staticmethod
    def get_estadisticas(cod_symbol):
        stmt = db.select(
            func.max(VariacionMensualModel.fch_ini_mes).label("max_fch_mes"),
            func.min(VariacionMensualModel.fch_ini_mes).label("min_fch_mes"),
            func.count(1).label("cantidad")
        ).where(
            VariacionMensualModel.symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        records = result.first()
        return records

    def get_variaciones_x_symbol(self, cod_symbol, cod_mes_desde, cod_mes_hasta, pandas=False):
        query = db.select(
            VariacionMensualModel
        ).where(
            VariacionMensualModel.symbol == cod_symbol,
            VariacionMensualModel.cod_mes >= cod_mes_desde,
            VariacionMensualModel.cod_mes <= cod_mes_hasta
        )

        if pandas is True:
            return pd.read_sql(query, db.get_engine())

        result = db.session.execute(query)
        return result.scalars().all()

    def get_variacion_x_semana(self, cod_symbol, cod_semana):
        query = db.select(
            VariacionMensualModel
        ).where(
            VariacionMensualModel.symbol == cod_symbol,
            VariacionMensualModel.cod_semana == cod_semana
        )

        result = db.session.execute(query)
        return result.scalars().first()

    @staticmethod
    def get_fch_mes_max(cod_symbol):
        query = db.select(
            func.max(VariacionMensualModel.fch_mes).label("fch_mes_max")
        ).where(
            VariacionMensualModel.cod_symbol == cod_symbol
        )

        result = db.session.execute(query)
        record = result.first()
        if record:
            return record.fch_mes_max