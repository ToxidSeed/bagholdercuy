from app import db

class MonedaModel(db.Model):
    __tablename__="tb_moneda"

    moneda_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(3))
    fec_registro = db.Column(db.Date)