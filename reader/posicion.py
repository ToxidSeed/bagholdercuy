from app import db
from model.posicion import PosicionModel
from model.OptionContract import OptionContractModel

import sqlalchemy.sql.functions as func
from sqlalchemy.sql import extract
from sqlalchemy.orm import join
from sqlalchemy import and_
from datetime import date

from config.negocio import TIPO_ACTIVO_OPT

class PosicionReader:

    def get_posiciones_abiertas(usuario_id, cod_symbol=None, cod_opcion=None):        

        stmt = db.select(
            PosicionModel
        ).where(
            PosicionModel.ctd_saldo_posicion != 0,
            PosicionModel.usuario_id == usuario_id
        ).order_by(
            PosicionModel.num_posicion.asc()
        )

        if cod_symbol is not None and cod_symbol != "":
            stmt.where(PosicionModel.cod_symbol == cod_symbol)
        else:
            stmt.where(PosicionModel.cod_opcion == cod_opcion)                    

        result = db.session.execute(stmt)       

        records = result.scalars().all()
        return records

    def get_posiciones_abiertas_x_opcion(usuario_id, cod_opcion):
        stmt = db.select(
            PosicionModel
        ).where(
            PosicionModel.ctd_saldo_posicion != 0,
            PosicionModel.usuario_id == usuario_id,
            PosicionModel.cod_opcion == cod_opcion
        ).order_by(
            PosicionModel.num_posicion.asc()
        )

        result = db.session.execute(stmt)       

        records = result.scalars().all()
        return records

    def get_posiciones_abiertas_x_symbol(usuario_id, cod_symbol):
        stmt = db.select(
            PosicionModel
        ).where(
            PosicionModel.ctd_saldo_posicion != 0,
            PosicionModel.usuario_id == usuario_id,
            PosicionModel.cod_symbol == cod_symbol
        ).order_by(
            PosicionModel.num_posicion.asc()
        )

        result = db.session.execute(stmt)       

        records = result.scalars().all()
        return records


    def get_max_num_posicion(usuario_id, fch_referencia, cod_symbol=None, cod_opcion=None):
 
        stmt = db.select(
            func.max(PosicionModel.num_posicion).label("num_posicion")
        ).where(
            PosicionModel.usuario_id == usuario_id,
            PosicionModel.fch_transaccion == fch_referencia          
        )

        if cod_symbol is not None and cod_symbol != "":
            stmt = stmt.where(PosicionModel.cod_symbol == cod_symbol)
        
        if cod_opcion is not None and cod_symbol != "":
            stmt = stmt.where(PosicionModel.cod_opcion == cod_opcion)        

        result = db.session.execute(stmt)
        record = result.first()
        
        if record is not None:
            return record.num_posicion
        else:
            return None

    
    def get_pos_abiertas_agrup_x_opcion(usuario_id, cod_opcion=None, cod_subyacente=None, anyo_expiracion=None, mes_expiracion=None
    , dia_expiracion=None, flg_call=True, flg_put=True):
        stmt = db.select(                        
            PosicionModel.cod_opcion,
            PosicionModel.cod_tipo_activo,
            func.min(PosicionModel.fch_transaccion).label('fch_primera_posicion'),
            func.sum(PosicionModel.ctd_saldo_posicion).label("ctd_saldo_posicion"),
            func.sum(PosicionModel.ctd_saldo_posicion * PosicionModel.imp_accion*100).label("imp_posicion_incial"),
            func.min(PosicionModel.imp_accion).label('imp_min_accion'),
            func.max(PosicionModel.imp_accion).label('imp_max_accion'),
            func.sum(PosicionModel.ctd_saldo_posicion*PosicionModel.imp_accion).label('imp_posicion'),
            (func.sum(PosicionModel.ctd_saldo_posicion * PosicionModel.imp_accion)/func.sum(PosicionModel.ctd_saldo_posicion)).label("imp_prom_accion")            
        ).select_from(
            PosicionModel
        ).join(
            OptionContractModel, and_(
                PosicionModel.cod_opcion == OptionContractModel.symbol,
                OptionContractModel.expiration_date >= date.today()
            )
        ).filter(
            PosicionModel.ctd_saldo_posicion != 0,            
            PosicionModel.usuario_id == usuario_id,
            PosicionModel.cod_tipo_activo == TIPO_ACTIVO_OPT
        ).group_by(
            PosicionModel.cod_symbol,
            PosicionModel.cod_opcion
        )

        if cod_opcion is not None:
            stmt = stmt.where(
                PosicionModel.cod_opcion == cod_opcion
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
            PosicionModel.cod_symbol,
            PosicionModel.cod_tipo_activo,
            func.min(PosicionModel.fch_transaccion).label('fch_primera_posicion'),
            func.sum(PosicionModel.ctd_saldo_posicion).label("ctd_saldo_posicion"),
            func.sum(PosicionModel.ctd_saldo_posicion * PosicionModel.imp_accion).label("imp_posicion_incial"),
            func.min(PosicionModel.imp_accion).label('imp_min_accion'),
            func.max(PosicionModel.imp_accion).label('imp_max_accion'),
            func.sum(PosicionModel.ctd_saldo_posicion*PosicionModel.imp_accion).label('imp_posicion'),
            (func.sum(PosicionModel.imp_accion)/func.sum(PosicionModel.ctd_saldo_posicion)).label("imp_prom_accion")            
        ).filter(
            PosicionModel.ctd_saldo_posicion != 0,            
            PosicionModel.usuario_id == usuario_id,
            PosicionModel.cod_tipo_activo != TIPO_ACTIVO_OPT
        ).group_by(
            PosicionModel.cod_symbol,
            PosicionModel.cod_opcion
        )

        result = db.session.execute(stmt)
        records = result.all()
        return records
    
    def get_operaciones(usuario_id):
        stmt = db.select(
            PosicionModel
        )

        results = db.session.execute(stmt)
        return results.scalars().all()