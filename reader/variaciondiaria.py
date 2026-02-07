from model.variaciondiaria import VariacionDiariaModel
from app import db
from sqlalchemy.sql import func
import pandas as pd


class VariacionDiariaReader:

    @staticmethod
    def get_max_fch_serie_anterior(cod_symbol, fch_ref):
        query = db.select(
            func.max(VariacionDiariaModel.fch_serie).label("fch_max_serie")
        ).where(
            VariacionDiariaModel.symbol == cod_symbol,
            VariacionDiariaModel.fch_serie < fch_ref
        )

        result = db.session.execute(query)
        return result.first()

    @staticmethod
    def get_max_fch_variacion(cod_symbol, fch_ref=None):
        query = db.select(
            func.max(VariacionDiariaModel.fch_serie).label("fch_max_variacion")
        ).where(
            VariacionDiariaModel.symbol == cod_symbol
        )

        if fch_ref is not None:
            query = query.where(                
                VariacionDiariaModel.fch_serie <= fch_ref
            )

        result = db.session.execute(query)
        record = result.first()
        if record is None:
            return None
            
        fch_max_variacion = record.fch_max_variacion
        return  fch_max_variacion


    @staticmethod
    def get_variacion_diaria_previa(cod_symbol, fch_serie):
        result = VariacionDiariaReader.get_max_fch_serie_anterior(cod_symbol, fch_serie)
        max_fch_serie_anterior = result.fch_max_serie

        query = db.select(
            VariacionDiariaModel
        ).where(
            VariacionDiariaModel.symbol == cod_symbol,
            VariacionDiariaModel.fch_serie == max_fch_serie_anterior
        )
        result = db.session.execute(query)
        return result.first()


    def get_variaciones_x_symbol(self, cod_symbol, fch_desde, fch_hasta, pandas=False):
        query = db.select(
            VariacionDiariaModel
        ).where(
            VariacionDiariaModel.symbol == cod_symbol,
            VariacionDiariaModel.fch_serie >= fch_desde,
            VariacionDiariaModel.fch_serie <= fch_hasta
        )

        if pandas is True:
            return pd.read_sql(query, db.get_engine())

        result = db.session.execute(query)
        return result.scalars().all()

    def get_valores_limites_entre_fechas(self, cod_symbol, fch_inicial, fch_final):
        query = db.select(
            func.max(VariacionDiariaModel.imp_maximo).label("imp_maximo"),
            func.min(VariacionDiariaModel.imp_minimo).label("imp_minimo")            
        ).where(
            VariacionDiariaModel.symbol == cod_symbol,
            VariacionDiariaModel.fch_serie >= fch_inicial,
            VariacionDiariaModel.fch_serie <= fch_final
        )

        result = db.session.execute(query)
        return result.first()

    @staticmethod
    def get_estadisticas(cod_symbol):
        query = db.select(
            func.max(VariacionDiariaModel.imp_maximo).label("imp_maximo"),
            func.min(VariacionDiariaModel.fch_serie).label("min_fch_variacion"),
            func.max(VariacionDiariaModel.fch_serie).label("max_fch_variacion"),
            func.min(VariacionDiariaModel.imp_minimo).label("imp_minimo"),
            func.count(1).label("cantidad")
        ).where(
            VariacionDiariaModel.symbol == cod_symbol
        )

        result = db.session.execute(query)
        return result.first()