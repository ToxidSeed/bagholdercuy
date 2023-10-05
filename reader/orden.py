from app import db

import sqlalchemy.sql.functions as func
from model.orden import OrdenModel

class OrdenReader:

    def get_max_num_orden(usuario_id, fch_orden, cod_symbol=None, cod_opcion=None):
        num_orden = None

        stmt = db.session.query(
            func.max(OrdenModel.num_orden).label("num_orden")
        ).filter(
            OrdenModel.usuario_id == usuario_id,            
            OrdenModel.fch_orden == fch_orden
        )

        if cod_symbol is not None and cod_symbol != "":
            stmt = stmt.where(OrdenModel.cod_symbol == cod_symbol)
        else:
            stmt = stmt.where(OrdenModel.cod_opcion == cod_opcion)           

        result = db.session.execute(stmt)
        record = result.first()

        if record is not None:
            num_orden = record.num_orden

        return num_orden

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

        
