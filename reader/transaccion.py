from app import db
from model.transaccion import TransaccionModel
from model.OptionContract import OptionContractModel
from model.calendariodiario import CalendarioDiarioModel
from model.StockSymbol import StockSymbol as StockSymbolModel

from reader.calendariosemanal import CalendarioSemanalReader

import sqlalchemy.sql.functions as func
from sqlalchemy.sql import extract
from sqlalchemy.orm import join
from sqlalchemy import and_
from datetime import date

from config.app_constants import TIPO_ACTIVO_OPT

class TransaccionReader:

    def get_transacciones_con_saldo(usuario_id, cod_symbol=None, cod_opcion=None):        

        stmt = db.select(
            TransaccionModel
        ).where(
            TransaccionModel.ctd_saldo_posicion != 0,
            TransaccionModel.usuario_id == usuario_id
        ).order_by(
            TransaccionModel.num_posicion.asc()
        )

        if cod_symbol is not None and cod_symbol != "":
            stmt.where(TransaccionModel.cod_symbol == cod_symbol)
        else:
            stmt.where(TransaccionModel.cod_opcion == cod_opcion)                    

        result = db.session.execute(stmt)       

        records = result.scalars().all()
        return records

    def get_transacciones_con_saldo_x_opcion(id_cuenta, id_contrato_opcion):
        stmt = db.select(
            TransaccionModel
        ).where(
            TransaccionModel.ctd_saldo_transaccion != 0,
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.id_contrato_opcion == id_contrato_opcion
        ).order_by(
            TransaccionModel.fch_transaccion.asc(),
            TransaccionModel.num_orden_transaccion.asc()
        )

        result = db.session.execute(stmt)       

        records = result.scalars().all()
        return records

    def get_transacciones_con_saldo_x_symbol(id_cuenta, id_symbol):
        stmt = db.select(
            TransaccionModel
        ).where(
            TransaccionModel.ctd_saldo_transaccion != 0,
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.id_symbol == id_symbol
        ).order_by(
            TransaccionModel.fch_transaccion.asc(),
            TransaccionModel.num_orden_transaccion.asc()
        )

        result = db.session.execute(stmt)       

        records = result.scalars().all()
        return records


    def get_max_num_posicion(id_cuenta, fch_referencia):
 
        stmt = db.select(
            func.max(TransaccionModel.num_orden_transaccion).label("num_orden_transaccion")
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.fch_transaccion == fch_referencia          
        )

        result = db.session.execute(stmt)
        record = result.first()
        
        if record is None:
            return 0
        
        if record.num_orden_transaccion is None:
            return 0
        
        return record.num_orden_transaccion

    def get_rentabilidad_x_semana(id_cuenta, fch_ini_semana, fch_fin_semana):
        stmt = db.select(
            func.sum(TransaccionModel.imp_rentabilidad).label("imp_rentabilidad")
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.fch_transaccion >= fch_ini_semana,
            TransaccionModel.fch_transaccion <= fch_fin_semana
        )

        result = db.session.execute(stmt)
        imp_rentabilidad = result.scalars().first()

        anyo, semana, dia = fch_fin_semana.isocalendar()

        return (anyo, semana, imp_rentabilidad)

    def get_rentabilidad_x_mes(id_cuenta, anyo, mes):
        stmt = db.select(
            func.sum(TransaccionModel.imp_rentabilidad).label("imp_rentabilidad")
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            extract("year",TransaccionModel.fch_transaccion) == anyo,
            extract("month",TransaccionModel.fch_transaccion) == mes
        )

        result = db.session.execute(stmt)
        return (anyo, mes, result.scalars().first())

    def get_rentabilidad_x_anyo(id_cuenta, anyo):
        stmt = db.select(
            func.sum(TransaccionModel.imp_rentabilidad).label("imp_rentabilidad")
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            extract("year", TransaccionModel.fch_transaccion) == anyo
        )

        result = db.session.execute(stmt)
        return (anyo, result.scalars().first())

    def get_rentabilidad_ultdia(id_cuenta):

        fch_ult_transaccion = TransaccionReader.get_ultdia_con_rentabilidad(id_cuenta=id_cuenta)

        stmt = db.select(
            TransaccionModel.fch_transaccion,
            func.sum(TransaccionModel.imp_rentabilidad).label("imp_rentabilidad")
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.fch_transaccion == fch_ult_transaccion
        ).group_by(
            TransaccionModel.fch_transaccion
        )

        result = db.session.execute(stmt)
        return result.first()

    def get_ultdia_con_rentabilidad(id_cuenta):
        stmt = db.session.query(
            func.max(TransaccionModel.fch_transaccion).label("fch_transaccion")
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.imp_rentabilidad != 0
        )

        result = db.session.execute(stmt)
        return result.scalars().first()

    def get_ultdia_transaccion(id_cuenta):

        stmt = db.session.query(
            func.max(TransaccionModel.fch_transaccion).label("fch_transaccion")
        ).where(
            TransaccionModel.id_cuenta == id_cuenta
        )

        result = db.session.execute(stmt)
        return result.scalars().first()

    def get_rentabilidad_diaria(id_cuenta, fch_desde, fch_hasta):
        stmt = db.select(
            TransaccionModel.id_cuenta,
            TransaccionModel.fch_transaccion,
            func.sum(TransaccionModel.imp_rentabilidad).label("imp_rentabilidad")
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.fch_transaccion >= fch_desde,
            TransaccionModel.fch_transaccion <= fch_hasta,
            TransaccionModel.imp_rentabilidad != 0
        ).group_by(
            TransaccionModel.id_cuenta,
            TransaccionModel.fch_transaccion
        ).order_by(
            TransaccionModel.fch_transaccion
        )

        result = db.session.execute(stmt)
        return result.all()

    def get_rentabilidad_semanal(id_cuenta, cod_semana_desde, cod_semana_hasta, flg_ascendente=True):
        stmt = db.select(
            TransaccionModel.id_cuenta, 
            TransaccionModel.cod_semana_transaccion,
            func.sum(TransaccionModel.imp_rentabilidad).label("imp_rentabilidad")
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.cod_mes_transaccion >= cod_semana_desde,
            TransaccionModel.cod_mes_transaccion <= cod_semana_hasta
        ).group_by(
            TransaccionModel.id_cuenta,
            TransaccionModel.cod_semana_transaccion
        ).order_by(
            TransaccionModel.id_cuenta
        )

        if flg_ascendente == True:
            stmt = stmt.order_by(
                TransaccionModel.cod_semana_transaccion.asc()
            )
        else:
            stmt = stmt.order_by(
                TransaccionModel.cod_semana_transaccion.desc()
            )

        result = db.session.execute(stmt)
        return result.all()
    
    def get_rentabilidad_mensual(id_cuenta, cod_mes_desde, cod_mes_hasta, flg_ascendente=True):
        """
        :param int fch_ini_mes: mes inicio desde el que se va a filtrar, formato yyyymm
        :param int mes_hasta: mes fin desde el que se va a filtrar, formato yyyymm
        """
        #fch_ini_mes = datetime.strptime(f"{cod_mes_desde}01","%Y%m%d")        

        stmt = db.select(
            TransaccionModel.id_cuenta,
            TransaccionModel.cod_mes_transaccion,            
            func.sum(TransaccionModel.imp_rentabilidad).label("imp_rentabilidad")
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.cod_mes_transaccion >= cod_mes_desde,
            TransaccionModel.cod_mes_transaccion <= cod_mes_hasta
        ).group_by(
            TransaccionModel.id_cuenta,
            TransaccionModel.cod_mes_transaccion
        ).order_by(
            TransaccionModel.id_cuenta            
        )

        if flg_ascendente is True:
            stmt = stmt.order_by(TransaccionModel.cod_mes_transaccion.asc())
        else:
            stmt = stmt.order_by(TransaccionModel.cod_mes_transaccion.desc())

        result = db.session.execute(stmt)
        return result.all()
    
    def get_rentabilidad_anual(id_cuenta, anyo_desde, anyo_hasta, orden="asc"):
        stmt = db.select(
            TransaccionModel.id_cuenta,
            extract("year",TransaccionModel.fch_transaccion).label("anyo_transaccion"),
            func.sum(TransaccionModel.imp_rentabilidad).label("imp_rentabilidad")
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            extract("year",TransaccionModel.fch_transaccion) >= anyo_desde,
            extract("year",TransaccionModel.fch_transaccion) <= anyo_hasta,
        ).group_by(
            TransaccionModel.id_cuenta,
            extract("year",TransaccionModel.fch_transaccion)
        )

        if orden == "asc":
            stmt = stmt.order_by(
                extract("year",TransaccionModel.fch_transaccion).asc()
            )
        
        if orden == "desc":
            stmt = stmt.order_by(
                extract("year",TransaccionModel.fch_transaccion).desc()
            )

        result = db.session.execute(stmt)
        return result.all()
        

    def get_rentabilidad_dias_calendarios(id_cuenta, fch_desde=None, fch_hasta=None):

        query = db.session.query(   
            TransaccionModel.id_cuenta,
            CalendarioDiarioModel.fch_dia.label("fch_transaccion"),
            func.sum(TransaccionModel.imp_rentabilidad).label("imp_rentabilidad")
        ).select_from(
            CalendarioDiarioModel
        ).outerjoin(
            TransaccionModel, and_(
                CalendarioDiarioModel.fch_dia == TransaccionModel.fch_transaccion,
                TransaccionModel.id_cuenta == id_cuenta
                )            
        ).where(            
            CalendarioDiarioModel.fch_dia >= fch_desde
        ).group_by(
            TransaccionModel.id_cuenta,
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

    def get_rentabilidad_ultsemana(id_cuenta):
        fch_ult_transaccion = TransaccionReader.get_ultdia_con_rentabilidad(id_cuenta=id_cuenta)        

        if fch_ult_transaccion is None:
            return (0, 0, 0)

        semana = CalendarioSemanalReader.get_semana_x_fecha(fch_referencia=fch_ult_transaccion)
        return TransaccionReader.get_rentabilidad_x_semana(id_cuenta=id_cuenta, fch_ini_semana=semana.fch_lunes, fch_fin_semana=semana.fch_viernes)

    def get_rentabilidad_ultmes(id_cuenta):
        fch_ult_transaccion = TransaccionReader.get_ultdia_con_rentabilidad(id_cuenta=id_cuenta)

        if fch_ult_transaccion is None:
            return (0, 0, 0)
            
        anyo_ult_transaccion = fch_ult_transaccion.year
        mes_ult_transaccion = fch_ult_transaccion.month
        return TransaccionReader.get_rentabilidad_x_mes(id_cuenta=id_cuenta, anyo=anyo_ult_transaccion, mes=mes_ult_transaccion)

    def get_rentabilidad_ultanyo(id_cuenta):
        fch_ult_transaccion = TransaccionReader.get_ultdia_con_rentabilidad(id_cuenta=id_cuenta)
        if fch_ult_transaccion is None:
            return (0, 0)

        anyo_ult_transaccion = fch_ult_transaccion.year
        return TransaccionReader.get_rentabilidad_x_anyo(id_cuenta=id_cuenta, anyo=anyo_ult_transaccion)        
    
    def get_pos_abiertas_agrup_x_contrato_opcion(id_cuenta):
        stmt = db.select(                        
            TransaccionModel.id_cuenta,
            TransaccionModel.id_symbol,
            TransaccionModel.id_contrato_opcion,
            OptionContractModel.symbol,
            func.min(TransaccionModel.fch_transaccion).label('fch_primera_posicion'),
            func.sum(TransaccionModel.ctd_saldo_transaccion).label("ctd_saldo_posicion"),
            func.sum(TransaccionModel.ctd_saldo_transaccion * TransaccionModel.imp_accion*100).label("imp_posicion_incial"),
            func.min(TransaccionModel.imp_accion).label('imp_min_accion'),
            func.max(TransaccionModel.imp_accion).label('imp_max_accion'),
            func.sum(TransaccionModel.ctd_saldo_transaccion * TransaccionModel.imp_accion).label('imp_posicion'),
            (func.sum(TransaccionModel.ctd_saldo_transaccion * TransaccionModel.imp_accion)/func.sum(TransaccionModel.ctd_saldo_transaccion)).label("imp_prom_accion")            
        ).select_from(
            TransaccionModel
        ).join(
            OptionContractModel, and_(
                TransaccionModel.id_contrato_opcion == OptionContractModel.id
            )
        ).filter(
            TransaccionModel.ctd_saldo_transaccion != 0,            
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.id_contrato_opcion != None
        ).group_by(
            TransaccionModel.id_cuenta,
            TransaccionModel.id_symbol,
            TransaccionModel.id_contrato_opcion,
            OptionContractModel.symbol
        )

        result = db.session.execute(stmt)
        records = result.all()
        return records

    def get_pos_abiertas_agrup_x_accion(id_cuenta):
        stmt = db.select(                        
            TransaccionModel.id_cuenta,
            TransaccionModel.id_symbol,
            StockSymbolModel.symbol,
            func.min(TransaccionModel.fch_transaccion).label('fch_primera_posicion'),
            func.sum(TransaccionModel.ctd_saldo_transaccion).label("ctd_saldo_posicion"),
            func.sum(TransaccionModel.ctd_saldo_transaccion * TransaccionModel.imp_accion).label("imp_posicion_incial"),
            func.min(TransaccionModel.imp_accion).label('imp_min_accion'),
            func.max(TransaccionModel.imp_accion).label('imp_max_accion'),
            func.sum(TransaccionModel.ctd_saldo_transaccion*TransaccionModel.imp_accion).label('imp_posicion'),
            (func.sum(TransaccionModel.imp_accion)/func.sum(TransaccionModel.ctd_saldo_transaccion)).label("imp_prom_accion")            
        ).select_from(
            TransaccionModel
        ).outerjoin(
            StockSymbolModel, and_(
                TransaccionModel.id_symbol == StockSymbolModel.id                
            )
        ).filter(            
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.ctd_saldo_transaccion != 0,
            TransaccionModel.id_contrato_opcion == None
        ).group_by(
            TransaccionModel.id_cuenta,
            TransaccionModel.id_symbol,
            StockSymbolModel.symbol
        )        

        result = db.session.execute(stmt)
        records = result.all()
        return records
    
    def get_operaciones(usuario_id):
        stmt = db.select(
            TransaccionModel
        )

        results = db.session.execute(stmt)
        return results.scalars().all()