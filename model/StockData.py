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
    u_open = db.Column(db.Numeric(15,4))
    u_high = db.Column(db.Numeric(15,4))
    u_low = db.Column(db.Numeric(15,4))
    u_close = db.Column(db.Numeric(15,4))
    u_volume = db.Column(db.Numeric(15,4))

    def from_iexcloud(self, element={}):
        self.symbol = element["symbol"]
        self.price_date = element["date"]
        self.open = element["open"]
        self.close = element["close"]
        self.high = element["high"]
        self.low = element["low"]
        self.volume = element["volume"]
        self.u_open = element["uOpen"]
        self.u_close = element["uClose"]
        self.u_high = element["uHigh"]
        self.u_low = element["uLow"]
        self.u_volume = element["uVolume"]
        return self