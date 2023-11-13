from app import db
from model.seriediaria import SerieDiariaModel
from model.CalendarioSemanal import CalendarioSemanalModel

import sqlalchemy.sql.functions as func
from sqlalchemy.sql import extract
from sqlalchemy import and_

from datetime import date

class SerieDiariaReader:
    
    @staticmethod
    def get_series_desde_fecha(symbol, fch_serie=None):
        
        stmt = db.select(
            SerieDiariaModel
        ).where(
            SerieDiariaModel.symbol == symbol
        )

        if fch_serie is not None:
            stmt = stmt.where(
                SerieDiariaModel.fch_serie >= fch_serie
            )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    def get_fch_serie_previa(symbol, fch_serie):
        stmt = db.select(
            func.max(SerieDiariaModel.fch_serie).label("fch_serie")
        ).where(
            SerieDiariaModel.symbol == symbol,
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
            SerieDiariaModel.symbol == symbol,
            SerieDiariaModel.fch_serie == fch_serie
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()
        return record

    def get_preseries_semanal(symbol, fch_ini_semana=None):

        stmt = db.select(
            SerieDiariaModel.symbol,
            CalendarioSemanalModel.fch_semana,
            CalendarioSemanalModel.anyo,
            CalendarioSemanalModel.semana,        
            func.min(SerieDiariaModel.fch_serie).label("open_date"),
            func.max(SerieDiariaModel.fch_serie).label("close_date"),
            func.min(SerieDiariaModel.imp_minimo).label("low"),
            func.max(SerieDiariaModel.imp_maximo).label("high"),
            func.min(SerieDiariaModel.imp_minimo_ajus).label("adj_low"),
            func.min(SerieDiariaModel.imp_maximo_ajus).label("adj_high"),                        
        ).select_from(
            SerieDiariaModel
        ).outerjoin(
            CalendarioSemanalModel,
            and_(
                SerieDiariaModel.fch_serie >= CalendarioSemanalModel.fch_inicio,
                SerieDiariaModel.fch_serie <= CalendarioSemanalModel.fch_fin
            )
        ).filter(
            SerieDiariaModel.symbol == symbol
        ).group_by(
            SerieDiariaModel.symbol,
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

    def get_preseries_mensual(symbol, fch_ini_mes):
        stmt = db.select(
            SerieDiariaModel.symbol,
            SerieDiariaModel.fch_mes,
            func.min(SerieDiariaModel.fch_serie).label("fch_apertura"),
            func.max(SerieDiariaModel.fch_serie).label("fch_cierre"),
            func.min(SerieDiariaModel.imp_minimo).label("imp_minimo"),
            func.max(SerieDiariaModel.imp_maximo).label("imp_maximo"),
            func.min(SerieDiariaModel.imp_minimo_ajus).label("imp_minimo_ajus"),
            func.min(SerieDiariaModel.imp_maximo_ajus).label("imp_maximo_ajus")
        ).where(
            SerieDiariaModel.symbol == symbol,            
        ).group_by(
            SerieDiariaModel.symbol,
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
            SerieDiariaModel.symbol,
            func.min(SerieDiariaModel.fch_serie).label("fch_serie_min")
        ).where(
            SerieDiariaModel.symbol == cod_symbol,
            SerieDiariaModel.fch_mes == fch_mes
        )

        result = db.session.execute(stmt)
        return result.first()

    def get_serie_anterior_a_fecha(self, cod_symbol, fch_serie, incluir_fecha=True):
        query = db.select(
            func.max(SerieDiariaModel.fch_serie).label("fch_serie")
        ).where(
            SerieDiariaModel.symbol == cod_symbol            
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
            SerieDiariaModel.symbol,
            func.max(SerieDiariaModel.fch_serie).label("fch_serie")
        ).group_by(
            SerieDiariaModel.symbol
        )

        if cod_symbol is not None:
            query = query.where(SerieDiariaModel.symbol == cod_symbol)                    

        result = db.session.execute(query)
        records = result.all()
        return records

    def get_series_entre_fechas(symbol, fch_inicio:date, fch_fin:date):
        stmt = """
        select
        symbol,
        fch_serie ,
        imp_apertura ,
        imp_maximo ,
        imp_minimo ,
        imp_cierre ,
        row_number() over (partition by symbol order by imp_maximo desc) as maxrow,
        row_number() over (partition by symbol order by imp_minimo asc) as minrow
        from tb_serie_diaria
        where symbol = '{0}'
        and fch_serie >= '{1}'
        and fch_serie <= '{2}'
        """

        stmt = stmt.format(symbol, fch_inicio.isoformat(), fch_fin.isoformat())
        result = db.session.execute(stmt)
        records = result.all()
        return records

        #stmt = stmt.format(symbol, fch_inicio, fch_fin.)