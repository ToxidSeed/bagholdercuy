from app import db

class StockData(db.Model):
    __tablename__= "tb_stock_data"

    id = db.Column(db.Integer,primary_key=True)
    symbol = db.Column(db.String(5))
    price_date = db.Column(db.Date)
    anyo = db.Column(db.Integer)
    mes = db.Column(db.Integer)
    semana = db.Column(db.Integer)
    frequency = db.Column(db.String(15))
    open = db.Column(db.Numeric(15,4))
    high = db.Column(db.Numeric(15,4))
    low = db.Column(db.Numeric(15,4))
    close = db.Column(db.Numeric(15,4))
    volume = db.Column(db.Numeric(15,4))
    adj_open = db.Column(db.Numeric(15,4))
    adj_high = db.Column(db.Numeric(15,4))
    adj_low = db.Column(db.Numeric(15,4))
    adj_close = db.Column(db.Numeric(15,4))
    adj_volume = db.Column(db.Numeric(15,4))
    split_factor = db.Column(db.Integer)    
    fch_registro = db.Column(db.Date)

    