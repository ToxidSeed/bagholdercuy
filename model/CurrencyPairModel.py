from app import db

class CurrencyPairModel(db.Model):
    __tablename__ = "tb_currency_pair"

    pair_id = db.Column(db.Integer, primary_key=True)
    currency_base_symbol = db.Column(db.String)
    currency_ref_symbol = db.Column(db.String)
    pair_name = db.Column(db.String)
    ind_activo = db.Column(db.String)
    fec_registro = db.Column(db.Date)
    fec_audit = db.Column(db.DateTime)