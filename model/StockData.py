from app import db

class StockData(db.Model):
    __tablename__= "tb_stock_data"

    id = db.Column(db.Integer,primary_key=True)
    symbol = db.Column(db.String(5))
    price_date = db.Column(db.Date)
    frequency = db.Column(db.String(15))
    open = db.Column(db.Numeric(15,4))
    high = db.Column(db.Numeric(15,4))
    low = db.Column(db.Numeric(15,4))
    close = db.Column(db.Numeric(15,4))
    volume = db.Column(db.Numeric(15,4))
