from model.variacionsemanal import VariacionSemanalModel
from app import db
from sqlalchemy.sql import func
import pandas as pd
import pandas as pd

class VariacionSemanalReader:

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