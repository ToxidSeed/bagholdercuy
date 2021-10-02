from app import db

class StockTrade(db.Model):
    __tablename__="tb_stock_trade"

    id = db.Column(db.Integer, primary_key=True)
    trade_group_id = db.Column(db.String(20))
    asset_type = db.Column(db.String(20))
    symbol	= db.Column(db.String(20))
    ref_trade_id = db.Column(db.Integer)
    trade_type = db.Column(db.String(1))
    shares_quantity = db.Column(db.Numeric(15,3))
    shares_balance = db.Column(db.Numeric(15,3))
    premium = db.Column(db.Numeric(15,3))
    trade_date = db.Column(db.Date)
    trade_month = db.Column(db.Integer)
    buy_price = db.Column(db.Numeric(17,3))
    buy_price_per_trade = db.Column(db.Numeric(17,3))
    sell_price = db.Column(db.Numeric(17,3))
    sell_price_per_trade = db.Column(db.Numeric(17,3))
    realized_gl = db.Column(db.Numeric(17,3))
    register_date = db.Column(db.Numeric(17,3))
    register_time = db.Column(db.Time)
