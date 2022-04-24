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
    split_factor = db.Column(db.Integer)    

    def from_iexcloud(self, element={}):
        self.symbol = element["symbol"]
        self.price_date = element["date"]
        self.open = element["open"]
        self.close = element["close"]
        self.high = element["high"]
        self.low = element["low"]
        self.volume = element["volume"]        
        return self