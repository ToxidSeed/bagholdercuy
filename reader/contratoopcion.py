from app import db
from model.contrato_opcion import ContratoOpcionModel

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
            ContratoOpcionModel
        ).where(
            ContratoOpcionModel.cod_symbol == cod_contrato_opcion
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()

        if record is not None and self.__buffer is True:
            self.__memoria[record.cod_symbol] = record   
        return record

    def get_calls( cod_subyacente, fch_expiracion=None, imp_ejercicio=None):
        stmt = db.select(
            ContratoOpcionModel
        ).where(
            ContratoOpcionModel.cod_symbol_subyacente == cod_subyacente,
            ContratoOpcionModel.tipo_opcion == "CALL"
        )

        if fch_expiracion is not None:
            stmt = stmt.where(
                ContratoOpcionModel.fch_vencimiento == fch_expiracion
            )

        if imp_ejercicio is not None:
            stmt = stmt.where(
                ContratoOpcionModel.imp_strike == imp_ejercicio
            )

        stmt = stmt.order_by(
            ContratoOpcionModel.fch_vencimiento.asc(),
            ContratoOpcionModel.imp_strike.asc()
        )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    @staticmethod
    def get_puts(cod_subyacente, fch_expiracion=None, imp_ejercicio=None):
        stmt = db.select(
            ContratoOpcionModel
        ).where(
            ContratoOpcionModel.cod_symbol_subyacente == cod_subyacente,
            ContratoOpcionModel.tipo_opcion == "PUT"
        )

        if fch_expiracion is not None:
            stmt = stmt.where(
                ContratoOpcionModel.fch_vencimiento == fch_expiracion
            )

        if imp_ejercicio is not None:
            stmt = stmt.where(
                ContratoOpcionModel.imp_strike == imp_ejercicio
            )

        stmt = stmt.order_by(
            ContratoOpcionModel.fch_vencimiento.asc(),
            ContratoOpcionModel.imp_strike.asc()
        )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    @staticmethod
    def get_fechas_expiracion(cod_subyacente, cod_tipo_opcion=None, imp_ejercicio=None):
        stmt = db.select(
            ContratoOpcionModel.fch_vencimiento
        ).where(
            ContratoOpcionModel.cod_symbol_subyacente == cod_subyacente
        )

        if cod_tipo_opcion in ["CALL", "PUT", "call", "put"]:
            stmt = stmt.where(
                ContratoOpcionModel.tipo_opcion == cod_tipo_opcion.upper()
            )

        if imp_ejercicio is not None:
            stmt = stmt.where(
                ContratoOpcionModel.imp_strike == imp_ejercicio
            )

        stmt = stmt.distinct()

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    @staticmethod
    def get_imp_ejercicios(cod_subyacente, cod_tipo_opcion=None, fch_expiracion=None):
        stmt = db.select(
            ContratoOpcionModel.imp_strike
        ).where(
            ContratoOpcionModel.cod_symbol_subyacente == cod_subyacente,
            ContratoOpcionModel.tipo_opcion == "PUT"
        )

        if cod_tipo_opcion in ["CALL", "PUT", "call", "put"]:
            stmt.where(
                ContratoOpcionModel.tipo_opcion == cod_tipo_opcion.upper()
            )

        if fch_expiracion is not None:
            stmt.where(
                ContratoOpcionModel.fch_vencimiento == fch_expiracion
            )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    @staticmethod
    def get_contratos(id_contrato_opcion=None, cod_subyacente=None, sentidos=[], fch_expiracion=None, imp_ejercicio=None, limit=0):

        stmt = db.select(
            ContratoOpcionModel
        )

        if id_contrato_opcion is not None:
            stmt = stmt.where(
                ContratoOpcionModel.id_contrato_opcion == id_contrato_opcion
            )

        if cod_subyacente is not None:
            stmt = stmt.where(
                ContratoOpcionModel.cod_symbol_subyacente == cod_subyacente
            )

        if len(sentidos) > 0:
            sentidos_upper = [s.upper() for s in sentidos]
            stmt = stmt.where(
                ContratoOpcionModel.tipo_opcion.in_(sentidos_upper)
            )
        
        if fch_expiracion is not None:
            stmt = stmt.where(
                ContratoOpcionModel.fch_vencimiento == fch_expiracion
            )
        
        if imp_ejercicio is not None:
            stmt = stmt.where(
                ContratoOpcionModel.imp_strike == imp_ejercicio
            )

        if limit > 0:
            stmt = stmt.limit(limit)

        stmt = stmt.order_by(
            ContratoOpcionModel.cod_symbol.asc()
        )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    @staticmethod
    def get_contrato(cod_symbol):
        stmt = db.select(
            ContratoOpcionModel
        ).where(
            ContratoOpcionModel.cod_symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()
        return record


