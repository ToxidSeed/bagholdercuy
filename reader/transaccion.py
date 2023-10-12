from app import db
from model.transaccion import TransaccionModel
from model.OptionContract import OptionContractModel

import sqlalchemy.sql.functions as func
from sqlalchemy.sql import extract
from sqlalchemy.orm import join
from sqlalchemy import and_
from datetime import date

from config.negocio import TIPO_ACTIVO_OPT

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

    def get_transacciones_con_saldo_x_opcion(usuario_id, cod_opcion):
        stmt = db.select(
            TransaccionModel
        ).where(
            TransaccionModel.ctd_saldo_posicion != 0,
            TransaccionModel.usuario_id == usuario_id,
            TransaccionModel.cod_opcion == cod_opcion
        ).order_by(
            TransaccionModel.num_posicion.asc()
        )

        result = db.session.execute(stmt)       

        records = result.scalars().all()
        return records

    def get_transacciones_con_saldo_x_symbol(usuario_id, cod_symbol):
        stmt = db.select(
            TransaccionModel
        ).where(
            TransaccionModel.ctd_saldo_posicion != 0,
            TransaccionModel.usuario_id == usuario_id,
            TransaccionModel.cod_symbol == cod_symbol
        ).order_by(
            TransaccionModel.num_posicion.asc()
        )

        result = db.session.execute(stmt)       

        records = result.scalars().all()
        return records


    def get_max_num_posicion(usuario_id, fch_referencia, cod_symbol=None, cod_opcion=None):
 
        stmt = db.select(
            func.max(TransaccionModel.num_posicion).label("num_posicion")
        ).where(
            TransaccionModel.usuario_id == usuario_id,
            TransaccionModel.fch_transaccion == fch_referencia          
        )

        if cod_symbol is not None and cod_symbol != "":
            stmt = stmt.where(TransaccionModel.cod_symbol == cod_symbol)
        
        if cod_opcion is not None and cod_symbol != "":
            stmt = stmt.where(TransaccionModel.cod_opcion == cod_opcion)        

        result = db.session.execute(stmt)
        record = result.first()
        
        if record is not None:
            return record.num_posicion
        else:
            return None

    
    def get_pos_abiertas_agrup_x_opcion(usuario_id, cod_opcion=None, cod_subyacente=None, anyo_expiracion=None, mes_expiracion=None
    , dia_expiracion=None, flg_call=True, flg_put=True):
        stmt = db.select(                        
            TransaccionModel.cod_opcion,
            TransaccionModel.cod_tipo_activo,
            func.min(TransaccionModel.fch_transaccion).label('fch_primera_posicion'),
            func.sum(TransaccionModel.ctd_saldo_posicion).label("ctd_saldo_posicion"),
            func.sum(TransaccionModel.ctd_saldo_posicion * TransaccionModel.imp_accion*100).label("imp_posicion_incial"),
            func.min(TransaccionModel.imp_accion).label('imp_min_accion'),
            func.max(TransaccionModel.imp_accion).label('imp_max_accion'),
            func.sum(TransaccionModel.ctd_saldo_posicion*TransaccionModel.imp_accion).label('imp_posicion'),
            (func.sum(TransaccionModel.ctd_saldo_posicion * TransaccionModel.imp_accion)/func.sum(TransaccionModel.ctd_saldo_posicion)).label("imp_prom_accion")            
        ).select_from(
            TransaccionModel
        ).join(
            OptionContractModel, and_(
                TransaccionModel.cod_opcion == OptionContractModel.symbol,
                OptionContractModel.expiration_date >= date.today()
            )
        ).filter(
            TransaccionModel.ctd_saldo_posicion != 0,            
            TransaccionModel.usuario_id == usuario_id,
            TransaccionModel.cod_tipo_activo == TIPO_ACTIVO_OPT
        ).group_by(
            TransaccionModel.cod_symbol,
            TransaccionModel.cod_opcion
        )

        if cod_opcion is not None:
            stmt = stmt.where(
                TransaccionModel.cod_opcion == cod_opcion
            )
        if cod_subyacente is not None:
            stmt = stmt.where(
                OptionContractModel.underlying == cod_subyacente
            )
                
        if anyo_expiracion is not None:
            stmt = stmt.where(
                extract("year", OptionContractModel.expiration_date) == anyo_expiracion
            )
        if mes_expiracion is not None:
            stmt = stmt.where(
                extract("month", OptionContractModel.expiration_date) == mes_expiracion
            )
        if dia_expiracion is not None:
            stmt = stmt.where(
                extract("day", OptionContractModel.expiration_date) == dia_expiracion
            )   

        tipos_opciones = []

        if flg_call == True:
            tipos_opciones.append("call")             
        
        if flg_put == True:
            tipos_opciones.append("put")

        if len(tipos_opciones) > 0:
            stmt = stmt.where(
                OptionContractModel.side.in_(tipos_opciones)
            )



        result = db.session.execute(stmt)
        records = result.all()
        return records

    def get_pos_abiertas_agrup_x_accion(usuario_id):
        stmt = db.select(                        
            TransaccionModel.cod_symbol,
            TransaccionModel.cod_tipo_activo,
            func.min(TransaccionModel.fch_transaccion).label('fch_primera_posicion'),
            func.sum(TransaccionModel.ctd_saldo_posicion).label("ctd_saldo_posicion"),
            func.sum(TransaccionModel.ctd_saldo_posicion * TransaccionModel.imp_accion).label("imp_posicion_incial"),
            func.min(TransaccionModel.imp_accion).label('imp_min_accion'),
            func.max(TransaccionModel.imp_accion).label('imp_max_accion'),
            func.sum(TransaccionModel.ctd_saldo_posicion*TransaccionModel.imp_accion).label('imp_posicion'),
            (func.sum(TransaccionModel.imp_accion)/func.sum(TransaccionModel.ctd_saldo_posicion)).label("imp_prom_accion")            
        ).filter(
            TransaccionModel.ctd_saldo_posicion != 0,            
            TransaccionModel.usuario_id == usuario_id,
            TransaccionModel.cod_tipo_activo != TIPO_ACTIVO_OPT
        ).group_by(
            TransaccionModel.cod_symbol,
            TransaccionModel.cod_opcion
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