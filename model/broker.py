from app import db

class BrokerModel(db.Model):
    __tablename__="tb_broker"

    id_broker=db.Column(db.Integer, primary_key=True)
    nom_broker=db.Column(db.String(250))
    flg_activo=db.Column(db.SmallInteger)
