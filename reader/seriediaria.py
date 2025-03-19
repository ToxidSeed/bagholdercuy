from app import db
from model.seriediaria import SerieDiariaModel
from model.CalendarioSemanal import CalendarioSemanalModel

import sqlalchemy.sql.functions as func
from sqlalchemy.sql import extract
from sqlalchemy import and_
from sqlalchemy.exc import ProgrammingError
from typing_extensions import deprecated

from datetime import date

class SerieDiariaReader:

    @staticmethod
    def get_series_desde_fecha(symbol, fch_serie=None):
        """
        Obtiene las series diarias desde una fecha determinada,
        * Si fch_serie es None devuelve todo
        """
        stmt = db.select(
            SerieDiariaModel
        ).where(
            SerieDiariaModel.cod_symbol == symbol
        )

        if fch_serie is not None:
            stmt = stmt.where(
                SerieDiariaModel.fch_serie >= fch_serie
            )

        stmt = stmt.order_by(
            SerieDiariaModel.fch_serie.asc()
        )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    @staticmethod
    def get_estadisticas(cod_symbol) -> SerieDiariaModel:
        stmt = db.select(
            func.max(SerieDiariaModel.fch_serie).label("max_fch_serie"),
            func.min(SerieDiariaModel.fch_serie).label("min_fch_serie"),
            func.count(1).label("cantidad")
        ).where(
            SerieDiariaModel.cod_symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()
        return record

    def get_fch_serie_previa(symbol, fch_serie):
        stmt = db.select(
            func.max(SerieDiariaModel.fch_serie).label("fch_serie")
        ).where(
            SerieDiariaModel.cod_symbol == symbol,
            SerieDiariaModel.fch_serie < fch_serie
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()
        return record

    @staticmethod
    def get_serie(symbol, fch_serie):
        stmt = db.select(
            SerieDiariaModel
        ).where(
            SerieDiariaModel.cod_symbol == symbol,
            SerieDiariaModel.fch_serie == fch_serie
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()
        return record

    def get_preseries_semanal(symbol, fch_ini_semana=None):

        stmt = db.select(
            SerieDiariaModel.cod_symbol,
            CalendarioSemanalModel.fch_semana,
            CalendarioSemanalModel.anyo,
            CalendarioSemanalModel.semana,        
            func.min(SerieDiariaModel.fch_serie).label("open_date"),
            func.max(SerieDiariaModel.fch_serie).label("close_date"),
            func.min(SerieDiariaModel.imp_minimo).label("imp_minimo"),
            func.max(SerieDiariaModel.imp_maximo).label("imp_maximo"),
            func.min(SerieDiariaModel.imp_minimo_sin_ajus).label("imp_minimo_sin_ajus"),
            func.min(SerieDiariaModel.imp_maximo_sin_ajus).label("imp_maximo_sin_ajus"),                        
        ).select_from(
            SerieDiariaModel
        ).outerjoin(
            CalendarioSemanalModel,
            and_(
                SerieDiariaModel.fch_serie >= CalendarioSemanalModel.fch_inicio,
                SerieDiariaModel.fch_serie <= CalendarioSemanalModel.fch_fin
            )
        ).filter(
            SerieDiariaModel.cod_symbol == symbol
        ).group_by(
            SerieDiariaModel.cod_symbol,
            CalendarioSemanalModel.fch_semana,
            CalendarioSemanalModel.anyo,
            CalendarioSemanalModel.semana
        ).order_by(
            CalendarioSemanalModel.fch_semana.asc()
        )

        if fch_ini_semana is not None:
            stmt = stmt.filter(
                SerieDiariaModel.fch_serie >= fch_ini_semana
            )
        
        result = db.session.execute(stmt)
        records = result.all()
        return records

    def get_preseries_mensual(symbol, fch_ini_mes=None):
        stmt = db.select(
            SerieDiariaModel.cod_symbol,
            SerieDiariaModel.fch_mes,
            func.min(SerieDiariaModel.fch_serie).label("fch_apertura"),
            func.max(SerieDiariaModel.fch_serie).label("fch_cierre"),
            func.min(SerieDiariaModel.imp_minimo).label("imp_minimo"),
            func.max(SerieDiariaModel.imp_maximo).label("imp_maximo"),
            func.min(SerieDiariaModel.imp_minimo_ajus).label("imp_minimo_ajus"),
            func.min(SerieDiariaModel.imp_maximo_ajus).label("imp_maximo_ajus")
        ).where(
            SerieDiariaModel.cod_symbol == symbol,            
        ).group_by(
            SerieDiariaModel.cod_symbol,
            SerieDiariaModel.fch_mes
        ).order_by(
            SerieDiariaModel.fch_mes.asc() 
        )

        if fch_ini_mes is not None:
            stmt = stmt.where(
                SerieDiariaModel.fch_serie >= fch_ini_mes
            )

        result = db.session.execute(stmt)
        records = result.all()
        return records

    def get_min_fecha_x_mes(cod_symbol, fch_mes):
        stmt = db.select(
            SerieDiariaModel.cod_symbol,
            func.min(SerieDiariaModel.fch_serie).label("fch_serie_min")
        ).where(
            SerieDiariaModel.cod_symbol == cod_symbol,
            SerieDiariaModel.fch_mes == fch_mes
        )

        result = db.session.execute(stmt)
        return result.first()

    def get_serie_anterior_a_fecha(cod_symbol, fch_serie, incluir_fecha=True):
        query = db.select(
            func.max(SerieDiariaModel.fch_serie).label("fch_serie")
        ).where(
            SerieDiariaModel.cod_symbol == cod_symbol            
        )

        if incluir_fecha is True:
            query = query.where(SerieDiariaModel.fch_serie <= fch_serie)
        else:
            query = query.where(SerieDiariaModel.fch_serie < fch_serie)

        result = db.session.execute(query)
        record_aux = result.first()

        if record_aux is None:
            return None
        
        return SerieDiariaReader.get_serie(symbol=cod_symbol, fch_serie=record_aux.fch_serie)

    def get_lista_fechas_maximas_x_symbol(self, cod_symbol=None):
        query = db.select(
            SerieDiariaModel.cod_symbol,
            func.min(SerieDiariaModel.fch_serie).label("min_fch_serie"),
            func.max(SerieDiariaModel.fch_serie).label("max_fch_serie"),
            func.count().label("num_series")
        ).group_by(
            SerieDiariaModel.cod_symbol
        )

        if cod_symbol is not None:
            query = query.where(SerieDiariaModel.cod_symbol == cod_symbol)                    

        result = db.session.execute(query)
        records = result.all()
        return records

    def get_fecha_maxima_x_symbol(self, cod_symbol=None):
        query = db.select(
            SerieDiariaModel.cod_symbol.label("cod_symbol"),
            func.max(SerieDiariaModel.fch_serie).label("max_fch_serie")
        ).where(
            SerieDiariaModel.cod_symbol == cod_symbol
        )

        result = db.session.execute(query)
        return result.first()

    @staticmethod
    def get_fecha_primera_serie(cod_symbol):
        query = db.select(
            func.min(SerieDiariaModel.fch_serie).label("fch_serie")
        ).where(
            SerieDiariaModel.cod_symbol == cod_symbol
        )

        result = db.session.execute(query)
        record = result.first()
        if record is not None:
            return record.fch_serie
        else:
            return None

    @staticmethod
    def get_series_entre_fechas(symbol, fch_inicio: date, fch_fin: date):

        query = db.select(
            SerieDiariaModel
        ).where(
            SerieDiariaModel.cod_symbol == symbol,
            SerieDiariaModel.fch_serie >= fch_inicio,
            SerieDiariaModel.fch_serie <= fch_fin
        )

        result = db.session.execute(query)
        records = result.scalars().all()
        return records

    
    @staticmethod
    @deprecated(" No usar porque la columna no tiene valor")
    def get_min_fch_serie_x_num_dias_separacion(cod_symbol, num_dias_separacion=0):
        stmt = db.select(
            SerieDiariaModel.cod_symbol,
            func.min(SerieDiariaModel.fch_serie).label("fch_serie")
        ).where(
            SerieDiariaModel.cod_symbol == cod_symbol,
            SerieDiariaModel.num_dias_serie_anterior >= num_dias_separacion
        ).group_by(
            SerieDiariaModel.cod_symbol
        )
        
        result = db.session.execute(stmt)
        return result.first()
        
        
        
        