from app import db

class CuentaModel(db.Model):
    __tablename__="tb_cuenta"

    id_cuenta = db.Column(db.Integer,primary_key=True)
    cod_cuenta = db.Column(db.String(15))
    nom_cuenta = db.Column(db.String(250))
    id_broker = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer)
    flg_activo = db.Column(db.SmallInteger)
