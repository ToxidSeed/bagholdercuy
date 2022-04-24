from app import db

class StockTrade(db.Model):
    __tablename__="tb_stock_trade"

    id = db.Column(db.Integer, primary_key=True)
    num_operacion = db.Column(db.Integer)
    asset_type = db.Column(db.String(20))
    symbol	= db.Column(db.String(20))
    ref_trade_id = db.Column(db.Integer)
    trade_type = db.Column(db.String(1))
    cantidad = db.Column(db.Numeric(15,3))
    saldo = db.Column(db.Numeric(15,3))
    premium = db.Column(db.Numeric(15,3))
    trade_date = db.Column(db.Date)
    trade_month = db.Column(db.Integer)
    imp_accion = db.Column(db.Numeric(17,2))
    imp_operacion = db.Column(db.Numeric(17,2))
    imp_accion_origen = db.Column(db.Numeric(17,2))
    realized_gl = db.Column(db.Numeric(17,2))
    register_date = db.Column(db.Date)
    register_time = db.Column(db.Time)
    user_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer)
