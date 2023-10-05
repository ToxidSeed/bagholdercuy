from app import db
from model.OptionContract import OptionContractModel

class OpcionReader:

    def get(symbol):

        stmt = db.select(
            OptionContractModel
        ).where(
            OptionContractModel.symbol == symbol
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()
        return record

    
    def get_contratos(cod_subyacente=None, sentidos=[], fch_expiracion=None, imp_ejercicio=0, limit=0):

        stmt = db.select(
            OptionContractModel
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
