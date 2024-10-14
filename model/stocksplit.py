from app import db

class StockSplitModel(db.Model):
    __tablename__ = "tb_stock_split"

    id_symbol = db.Column(db.Integer,primary_key=True)
    cod_symbol = db.Column(db.String)
    fch_split = db.Column(db.Date,primary_key=True)
    numerador = db.Column(db.Integer)
    denominador = db.Column(db.Integer)