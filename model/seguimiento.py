from app import db

class SeguimientoModel(db.Model):
    __tablename__ = 'tb_seguimiento'

    id_seguimiento = db.Column(db.Integer,primary_key=True,nullable=False)
    id_cuenta = db.Column(db.Integer,nullable=False)
    id_symbol = db.Column(db.Integer,nullable=False)
    fch_registro = db.Column(db.Date)