from app import db

class TransaccionFondosModel(db.Model):
    __tablename__="tb_transaccion_fondos"

    id = db.Column(db.Integer,primary_key=True)
    ref_transaccion_id = db.Column(db.Integer)
    ref_externa_id = db.Column(db.Integer)
    fec_transaccion = db.Column(db.Date)
    est_transaccion_fondos_id = db.Column(db.Integer)
    tipo_transaccion = db.Column(db.String(1))
    subtipo_transaccion = db.Column(db.String(1))
    importe = db.Column(db.Numeric(15,2))
    concepto = db.Column(db.String(250))
    moneda_symbol = db.Column(db.String(3))
    saldo = db.Column(db.Numeric(15,2))
    user_id = db.Column(db.Integer)
    fec_registro = db.Column(db.Date)
    fec_audit = db.Column(db.DateTime)

