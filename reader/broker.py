from model.broker import BrokerModel
from app import db

class BrokerReader:
    def get_brokers_activos():

        stmt = db.select(
            BrokerModel
        )

        result = db.session.execute(stmt)
        return result.scalars().all()

    def get_brokers(args={}):
        stmt = db.select(
            BrokerModel
        )

        nombre = args.get("nombre")
        if nombre is not None:            
            stmt = stmt.where(
                BrokerModel.nom_broker.ilike("%{}%".format(nombre))
            )

        flg_activo = args.get("flg_activo")
        if flg_activo is not None:
            stmt = stmt.where(
                BrokerModel.flg_activo == flg_activo
            )

        result = db.session.execute(stmt)
        return result.scalars().all()

    def get(id_broker):
        stmt = db.select(
            BrokerModel
        ).where(
            BrokerModel.id_broker == id_broker
        )

        result = db.session.execute(stmt)
        return result.scalars().one()

