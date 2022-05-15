from app import db

class OrderModel(db.Model):
    __tablename__ = "tb_order"

    order_id = db.Column(db.Integer, primary_key=True)
    num_orden = db.Column(db.Integer)
    order_type = db.Column(db.String(1))
    symbol = db.Column(db.String(20))
    asset_type = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(15,4))
    register_date = db.Column(db.Date)
    order_date = db.Column(db.Date)
