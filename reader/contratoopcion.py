from app import db
from model.OptionContract import OptionContractModel

class ContratoOpcionReader:
    def __init__(self, buffer=False):
        self.__buffer = buffer
        self.__memoria = {}

    def get(self, cod_contrato_opcion):
        if self.__buffer is True:
            record = self.__memoria.get(cod_contrato_opcion)
        
            if record is not None:
                return record

        #consultamos eb base de datos
        stmt = db.select(
            OptionContractModel
        ).where(
            OptionContractModel.symbol == cod_contrato_opcion
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()

        if record is not None and self.__buffer is True:
            self.__memoria[record.cod_symbol] = record   
        return record

    
    def get_contratos(id_contrato_opcion=None, cod_subyacente=None, sentidos=[], fch_expiracion=None, imp_ejercicio=0, limit=0):

        stmt = db.select(
            OptionContractModel
        )

        if id_contrato_opcion is not None:
            stmt = stmt.where(
                OptionContractModel.id == id_contrato_opcion
            )

        if cod_subyacente is not None:
            stmt = stmt.where(
                OptionContractModel.underlying == cod_subyacente
            )

        if len(sentidos) > 0:
            stmt = stmt.where(
                OptionContractModel.side.in_(sentidos)
            )
        
        if fch_expiracion is not None:
            stmt = stmt.where(
                OptionContractModel.expiration_date == fch_expiracion
            )
        
        if imp_ejercicio > 0:
            stmt = stmt.where(
                OptionContractModel.strike == imp_ejercicio
            )

        if limit > 0:
            stmt = stmt.limit(limit)

        stmt = stmt.order_by(
            OptionContractModel.symbol.asc()
        )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records
