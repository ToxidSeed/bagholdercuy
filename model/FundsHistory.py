from app import db

class FundsHistory(db.Model):
    __tablename__ = 'tb_funds_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    fec_registro = db.Column(db.Date)
    estado_id = db.Column(db.Integer)
    tipo_transaccion = db.Column(db.String(1))
    importe = db.Column(db.Numeric(15,2))
    concepto = db.Column(db.String(250))
    moneda_symbol = db.Column(db.String(3))
    