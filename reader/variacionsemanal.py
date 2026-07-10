from model.variacionsemanal import VariacionSemanalModel
from config.extensions import db
from sqlalchemy.sql import func
import pandas as pd


class VariacionSemanalReader:

    @staticmethod
    def get_estadisticas(cod_symbol):
        stmt = db.select(
            func.max(VariacionSemanalModel.cod_semana).label("max_cod_semana"),
            func.min(VariacionSemanalModel.cod_semana).label("min_cod_semana"),
            func.max(VariacionSemanalModel.fecha).label("fch_semana_max"),
            func.min(VariacionSemanalModel.fecha).label("fch_semana_min"),
            func.count(1).label("cantidad")
        ).where(
            VariacionSemanalModel.symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        records = result.first()
        return records

    def get_variaciones_x_symbol(self, cod_symbol, cod_semana_desde, cod_semana_hasta, pandas=False):
        query = db.select(
            VariacionSemanalModel
        ).where(
            VariacionSemanalModel.symbol == cod_symbol,
            VariacionSemanalModel.cod_semana >= cod_semana_desde,
            VariacionSemanalModel.cod_semana <= cod_semana_hasta
        )

        if pandas is True:
            return pd.read_sql(query, db.get_engine())

        result = db.session.execute(query)
        return result.scalars().all()

    def get_variacion_x_semana(self, cod_symbol, cod_semana):
        query = db.select(
            VariacionSemanalModel
        ).where(
            VariacionSemanalModel.symbol == cod_symbol,
            VariacionSemanalModel.cod_semana == cod_semana
        )

        result = db.session.execute(query)
        return result.scalars().first()

    @staticmethod
    def get_max_fch_variacion(cod_symbol):
        query = db.select(
            func.max(VariacionSemanalModel.fecha).label("fch_semana_var")
        ).where(
            VariacionSemanalModel.symbol == cod_symbol
        )

        result = db.session.execute(query)
        record = result.first()
        if record:
            return record.fch_semana_var

    @staticmethod
    def get_variaciones_desde_fecha(cod_symbol, fch_semana):
        query = db.select(
            VariacionSemanalModel
        ).where(
            VariacionSemanalModel.symbol == cod_symbol,
        )

        if fch_semana:
            query = query.where(
                VariacionSemanalModel.fecha >= fch_semana
            )
                    
        result = db.session.execute(query)
        records = result.scalars().all()
        return records
