from app import db

class StockSymbol(db.Model):
    __tablename__="tb_stock_symbol"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20))
    name = db.Column(db.String(250))
    exchange = db.Column(db.String(15))
    asset_type = db.Column(db.String(15))