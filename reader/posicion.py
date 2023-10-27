from model.posicion import PosicionModel
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