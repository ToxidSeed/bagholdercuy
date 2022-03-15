from app import db

class CurrencyModel(db.Model):
    __tablename__="tb_currency"

    currency_id = db.Column(db.Integer, primary_key=True)
    currency_symbol = db.Column(db.String(3))
    currency_name = db.Column(db.String(15))
    currency_desc = db.Column(db.String(50))
    fec_registro = db.Column(db.Date)
    fec_audit = db.Column(db.DateTime)    