from app import db

class OptionContract(db.Model):
    __tablename__ = "tb_option_contract"

    id = db.Column(db.Integer, primary_key=True)
    symbol_id = db.Column(db.Integer)
    contract_size = db.Column(db.Integer)
    currency = db.Column(db.String(5))
    description = db.Column(db.String(250))
    expiration_date = db.Column(db.Date)
    side = db.Column(db.String(4))
    strike = db.Column(db.Numeric(15,2))
    symbol = db.Column(db.String(50))
    underlying = db.Column(db.String(5))
    register_date = db.Column(db.Date)