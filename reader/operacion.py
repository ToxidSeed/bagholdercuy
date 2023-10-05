from app import db
import sqlalchemy.sql.functions as func
from sqlalchemy.sql import extract
from sqlalchemy import and_

from model.posicion import PosicionModel
from model.calendariodiario import CalendarioDiarioModel
from reader.calendariosemanal import CalendarioSemanalReader

class OperacionReader:

    """def get_max_num_operacion(usuario_id, symbol, fch_referencia):
        num_operacion = None

        result = db.session.query(
            func.max(StockTrade.num_operacion).label("num_operacion")
        ).\
        filter(
            StockTrade.usuario_id == usuario_id,
            StockTrade.trade_date == fch_referencia,
            StockTrade.symbol == symbol
        ).first()           

        if result is None:
            num_operacion = result.num_operacion 

        return num_operacion"""

    def get_rentabilidad_diaria(usuario_id, fch_desde=None, fch_hasta=None):

        query = db.session.query(   
            PosicionModel.usuario_id,
            CalendarioDiarioModel.fch_dia.label("fch_transaccion"),
            func.sum(PosicionModel.imp_gp_realizada).label("imp_rentabilidad")
        ).select_from(
            CalendarioDiarioModel
        ).outerjoin(
            PosicionModel, and_(
                CalendarioDiarioModel.fch_dia == PosicionModel.fch_transaccion,
                PosicionModel.usuario_id == usuario_id
                )            
        ).where(            
            CalendarioDiarioModel.fch_dia >= fch_desde
        ).group_by(
            PosicionModel.usuario_id,
            CalendarioDiarioModel.fch_dia
        ).order_by(
            CalendarioDiarioModel.fch_dia.desc()
        )

        if fch_hasta is not None:
            query = query.where( 
                CalendarioDiarioModel.fch_dia <= fch_hasta
            )

        result = db.session.execute(query)                

        records = result.all()
        return records

    def get_rentabilidad_x_semana(usuario_id, fch_ini_semana, fch_fin_semana):
        stmt = db.select(
            func.sum(PosicionModel.imp_gp_realizada).label("imp_rentabilidad")
        ).where(
            PosicionModel.usuario_id == usuario_id,
            PosicionModel.fch_transaccion >= fch_ini_semana,
            PosicionModel.fch_transaccion <= fch_fin_semana
        )

        result = db.session.execute(stmt)
        imp_rentabilidad = result.scalars().first()

        anyo, semana, dia = fch_fin_semana.isocalendar()

        return (anyo, semana, imp_rentabilidad)

    def get_rentabilidad_x_mes(usuario_id, anyo, mes):
        stmt = db.select(
            func.sum(PosicionModel.imp_gp_realizada).label("imp_rentabilidad")
        ).where(
            PosicionModel.usuario_id == usuario_id,
            extract("year",PosicionModel.fch_transaccion) == anyo,
            extract("month",PosicionModel.fch_transaccion) == mes
        )

        result = db.session.execute(stmt)
        return (anyo, mes, result.scalars().first())

    def get_rentabilidad_x_anyo(usuario_id, anyo):
        stmt = db.select(
            func.sum(PosicionModel.imp_gp_realizada).label("imp_rentabilidad")
        ).where(
            PosicionModel.usuario_id == usuario_id,
            extract("year", PosicionModel.fch_transaccion) == anyo
        )

        result = db.session.execute(stmt)
        return (anyo, result.scalars().first())

    def get_rentabilidad_ultdia(usuario_id=1):

        fch_ult_transaccion = OperacionReader.get_ultdia_transaccion(usuario_id=usuario_id)

        stmt = db.select(
            PosicionModel.fch_transaccion,
            func.sum(PosicionModel.imp_gp_realizada).label("imp_rentabilidad")
        ).where(
            PosicionModel.usuario_id == usuario_id,
            PosicionModel.fch_transaccion == fch_ult_transaccion
        ).group_by(
            PosicionModel.fch_transaccion
        )

        result = db.session.execute(stmt)
        return result.first()

    def get_rentabilidad_ultsemana(usuario_id):

        fch_ult_transaccion = OperacionReader.get_ultdia_transaccion(usuario_id=usuario_id)
        semana = CalendarioSemanalReader.get_semana_x_fecha(fch_referencia=fch_ult_transaccion)
        return OperacionReader.get_rentabilidad_x_semana(usuario_id=usuario_id, fch_ini_semana=semana.fch_lunes, fch_fin_semana=semana.fch_viernes)

    def get_rentabilidad_ultmes(usuario_id):
        fch_ult_transaccion = OperacionReader.get_ultdia_transaccion(usuario_id=usuario_id)
        anyo_ult_transaccion = fch_ult_transaccion.year
        mes_ult_transaccion = fch_ult_transaccion.month
        return OperacionReader.get_rentabilidad_x_mes(usuario_id=usuario_id, anyo=anyo_ult_transaccion, mes=mes_ult_transaccion)

    def get_rentabilidad_ultanyo(usuario_id):
        fch_ult_transaccion = OperacionReader.get_ultdia_transaccion(usuario_id=usuario_id)
        anyo_ult_transaccion = fch_ult_transaccion.year
        return OperacionReader.get_rentabilidad_x_anyo(usuario_id=usuario_id, anyo=anyo_ult_transaccion)        

    def get_ultdia_transaccion(usuario_id):

        stmt = db.session.query(
            func.max(PosicionModel.fch_transaccion).label("fch_transaccion")
        ).where(
            PosicionModel.usuario_id == usuario_id
        )

        result = db.session.execute(stmt)
        return result.scalars().first()


