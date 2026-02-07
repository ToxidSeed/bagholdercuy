from app import db

import sqlalchemy.sql.functions as func
from model.orden import OrdenModel

class OrdenReader:

    def get_max_num_orden(id_cuenta, fch_orden):        

        stmt = db.session.query(
            func.max(OrdenModel.num_orden).label("num_orden")
        ).filter(
            OrdenModel.id_cuenta == id_cuenta,            
            OrdenModel.fch_orden == fch_orden
        )

        result = db.session.execute(stmt)
        record = result.first()

        if record is None:
            return 0
        if record.num_orden is None:
            return 0
        else:
            return 0

    def get_ordenes(id_cuenta, id_symbol=None, id_contrato_opcion=None):
        stmt = db.session.query(
            OrdenModel.id_orden,
            OrdenModel.id_operacion,
            OrdenModel.id_cuenta,
            OrdenModel.num_orden,
            OrdenModel.cod_tipo_orden,
            OrdenModel.id_symbol,
            OrdenModel.id_contrato_opcion,
            OrdenModel.cod_tipo_activo,
            OrdenModel.cantidad,
            OrdenModel.imp_accion,
            OrdenModel.fch_registro,
            OrdenModel.fch_orden
        ).join(
            
        ).where(
            OrdenModel.id_cuenta == id_cuenta
        )

        result = db.session.execute(stmt)
        return result.scalars().all()

        
