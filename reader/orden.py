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

    def get_ordenes(usuario_id, cod_symbol=None, cod_opcion=None):
        stmt = db.session.query(
            OrdenModel
        ).where(
            OrdenModel.usuario_id == usuario_id
        )

        if cod_symbol is not None:
            stmt = stmt.where(
                OrdenModel.cod_symbol == cod_symbol
            )

        if cod_opcion is not None:
            stmt = stmt.where(
                OrdenModel.cod_opcion == cod_opcion
            )

        stmt = stmt.order_by(
            OrdenModel.fch_orden,
            OrdenModel.cod_opcion,
            OrdenModel.cod_symbol
        )

        result = db.session.execute(stmt)
        return result.scalars().all()

        
