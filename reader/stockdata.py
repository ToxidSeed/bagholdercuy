from model.StockData import StockData
from model.CalendarioSemanal import CalendarioSemanalModel
from app import db
from config.negocio import TIPO_FRECUENCIA_SERIE_DIARIA

from sqlalchemy import func,and_,extract
from sqlalchemy.orm import join
import warnings

class StockDataReader:
    def get_series_diarias(symbol, fch_inicio=None):
        stmt = db.select(StockData).where(
            StockData.symbol == symbol,
            StockData.frequency == TIPO_FRECUENCIA_SERIE_DIARIA
        )

        if fch_inicio is not None:
            stmt = stmt.where(StockData.price_date >= fch_inicio)
        
        return db.session.execute(stmt)

    def get_series_diarias_asc(symbol, fch_inicio=None):
        stmt = db.select(StockData).where(
            StockData.symbol == symbol,
            StockData.frequency == TIPO_FRECUENCIA_SERIE_DIARIA
        )

        if fch_inicio is not None:
            stmt = stmt.where(StockData.price_date >= fch_inicio)
        
        stmt = stmt.order_by(StockData.price_date.asc())
        
        return db.session.execute(stmt)
    
    warnings.warn("deprecated", DeprecationWarning)
    def get_base_semanal(symbol,fch_ini_semana=None):
        query = db.session.query(
            CalendarioSemanalModel.fch_semana,
            CalendarioSemanalModel.anyo,
            CalendarioSemanalModel.semana,
            StockData.symbol,
            func.min(StockData.price_date).label("open_date"),
            func.max(StockData.price_date).label("close_date"),
            func.min(StockData.low).label("low"),
            func.max(StockData.high).label("high"),
            func.min(StockData.adj_low).label("adj_low"),
            func.min(StockData.adj_high).label("adj_high"),                        
        ).select_from(
            StockData
        ).outerjoin(
            CalendarioSemanalModel,
            and_(
                StockData.anyo == CalendarioSemanalModel.anyo,
                StockData.semana == CalendarioSemanalModel.semana
            )
        ).filter(
            and_(
                StockData.frequency == "daily",
                StockData.symbol == symbol
            )
        ).group_by(
            StockData.symbol,
            CalendarioSemanalModel.fch_semana
        ).order_by(
            CalendarioSemanalModel.fch_semana.asc()
        )

        if fch_ini_semana is not None:
            query = query.filter(
                StockData.price_date >= fch_ini_semana
            )
        
        return query.all()

    def get_base_mensual(symbol, fch_ini_mes):

        stmt = db.select(
            StockData.symbol,
            extract("year",StockData.price_date).label("anyo"),
            extract("month",StockData.price_date).label("mes"),
            func.min(StockData.price_date).label("open_date"),
            func.max(StockData.price_date).label("close_date"),
            func.min(StockData.low).label("low"),
            func.max(StockData.high).label("high"),
            func.min(StockData.adj_low).label("adj_low"),
            func.min(StockData.adj_high).label("adj_high")
        ).where(
            StockData.symbol == symbol,
            StockData.frequency == 'daily'
        ).group_by(
            StockData.symbol,
            extract("year",StockData.price_date),
            extract("month",StockData.price_date)
        ).order_by(
            extract("year",StockData.price_date).asc(),
            extract("month",StockData.price_date).asc()
        )

        if fch_ini_mes is not None:

            stmt = stmt.where(
                StockData.price_date >= fch_ini_mes
            )

        return db.session.execute(stmt)                 


    def get_serie(symbol, fecha):

        query = db.select(
            StockData
        ).where(
            StockData.symbol == symbol,
            StockData.price_date == fecha,
            StockData.frequency == 'daily'
        )

        record = db.session.execute(query)        
        return record.scalars().one()

    def get_serie_semanal(symbol, anyo, semana):
        query = db.select(
            StockData
        ).filter(
            StockData.symbol == symbol,
            StockData.frequency == 'weekly',
            StockData.semana == semana
        )

        results = db.session.execute(query)
        return results.fetchone()

    