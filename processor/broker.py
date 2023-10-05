from model.broker import BrokerModel
from reader.broker import BrokerReader
from app import db

class BrokerProcessor:
    def guardar(self, broker:BrokerModel):
        if broker.id_broker is None:
            db.session.add(broker)
        else:
            broker_a_actualizar = BrokerReader.get(broker.id_broker)
            broker_a_actualizar.nom_broker = broker.nom_broker
            broker_a_actualizar.flg_activo = broker.flg_activo

        
