from app import db

class FundsHistory(db.Model):
    __tablename__ = 'tb_funds_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    fec_registro = db.Column(db.Date)
    estado_id = db.Column(db.Integer)
    flg_tipo_movimiento = db.Column(db.String(1))
    importe = db.Column(db.Numeric(15,2))
    concepto = db.Column(db.String(250))
    