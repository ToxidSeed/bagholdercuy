from model.operacion import OperacionModel
from app import db
from sqlalchemy.sql.functions import func

class OperacionReader:

    def get_max_num_orden(id_cuenta, fch_operacion):
        query = db.select(
            func.max(OperacionModel.num_orden).label('num_orden')
        ).where(
            OperacionModel.id_cuenta == id_cuenta,
            OperacionModel.fch_operacion == fch_operacion
        )

        result = db.session.execute(query)
        record = result.first()

        if record is None:
            return 0
        
        if record.num_orden is None:
            return 0
        
        return record.num_orden

    def get(id_operacion):
        query = db.select(
            OperacionModel
        ).where(
            OperacionModel.id_operacion == id_operacion
        )

        result = db.session.execute(query)
        record = result.scalars().first()
        return record

    def get_ultima_fecha_operacion(id_cuenta, id_symbol, id_contrato_opcion):
        query = db.select(
            func.max(OperacionModel.fch_operacion).label("fch_operacion")
        ).where(
            OperacionModel.id_cuenta == id_cuenta,
            OperacionModel.id_symbol == id_symbol,
            OperacionModel.id_contrato_opcion == id_contrato_opcion
        )

        result = db.session.execute(query)
        record = result.first()

        if record is None:
            return None
        
        if record.fch_operacion is None:
            return None
        
        return record.fch_operacion
