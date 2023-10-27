from model.posicion import PosicionModel
from model.OptionContract import OptionContractModel
from model.StockSymbol import StockSymbol
from app import db

class PosicionReader:
    def get(id_posicion):
        query = db.select(
            PosicionModel
        ).where(
            PosicionModel.id_posicion == id_posicion
        )

        result = db.session.execute(query)
        record = result.scalars().first()
        return record
    
    def get_pos_abiertas_agrup_x_accion(id_cuenta):
        stmt = db.select(
            PosicionModel.id_posicion,
            PosicionModel.id_cuenta,
            PosicionModel.id_symbol,
            PosicionModel.id_contrato_opcion,
            PosicionModel.id_ultima_operacion,
            PosicionModel.cantidad,
            PosicionModel.imp_promedio,
            PosicionModel.imp_maximo,
            PosicionModel.imp_minimo,
            PosicionModel.fch_registro,
            PosicionModel.fch_ultima_actualizacion,
            StockSymbol.symbol, 
            StockSymbol.name
        ).select_from(
            PosicionModel
        ).join(
            StockSymbol, PosicionModel.id_symbol == StockSymbol.id
        ).where(
            PosicionModel.id_cuenta == id_cuenta, 
            PosicionModel.cantidad != 0,
            PosicionModel.id_contrato_opcion == None
        )

        result = db.session.execute(stmt)
        records = result.all()
        return records
    
    def get_pos_abiertas_agrup_x_contrato_opcion(id_cuenta):
        stmt = db.select(
            PosicionModel.id_posicion,
            PosicionModel.id_cuenta,
            PosicionModel.id_symbol,
            PosicionModel.id_contrato_opcion,
            PosicionModel.id_ultima_operacion,
            PosicionModel.cantidad,
            PosicionModel.imp_promedio,
            PosicionModel.imp_maximo,
            PosicionModel.imp_minimo,
            PosicionModel.fch_registro,
            PosicionModel.fch_ultima_actualizacion,
            OptionContractModel.symbol,
            OptionContractModel.underlying.label("cod_subyacente"),
            OptionContractModel.expiration_date.label("fch_expiracion"), 
            OptionContractModel.side.label("cod_tipo_opcion"),
            OptionContractModel.strike.label("imp_ejercicio")
        ).select_from(
            PosicionModel            
        ).join(
            OptionContractModel, PosicionModel.id_contrato_opcion == OptionContractModel.id
        ).where(
            PosicionModel.id_cuenta == id_cuenta, 
            PosicionModel.cantidad != 0,
            PosicionModel.id_contrato_opcion != None
        )

        result = db.session.execute(stmt)
        records = result.all()
        return records

    def get_x_instrumento(id_cuenta, id_symbol, id_contrato_opcion=None):

        query = db.select(
            PosicionModel
        ).where(
            PosicionModel.id_cuenta == id_cuenta,
            PosicionModel.id_symbol == id_symbol,
            PosicionModel.id_contrato_opcion == id_contrato_opcion
        )

        result = db.session.execute(query)
        record = result.scalars().first()
        return record