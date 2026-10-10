from config.extensions import db

class SymbolModel(db.Model):
    __tablename__="tb_symbol"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), unique=True)
    id_symbol_type = db.Column(db.Integer)
    name = db.Column(db.String(250))
    moneda_id = db.Column(db.String(3))
    region = db.Column(db.String(10))
    exchange = db.Column(db.String(15))
    asset_type = db.Column(db.String(15))
    fec_registro = db.Column(db.Date)
    fec_audit = db.Column(db.DateTime)
