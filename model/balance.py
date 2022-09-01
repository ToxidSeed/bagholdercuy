from app import db

class BalanceCuentaModel(db.Model):
    __tablename__ = "tb_balance_cuenta"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    moneda_id = db.Column(db.String(3))
    imp_saldo = db.Column(db.Numeric(15,2))
    imp_inversion = db.Column(db.Numeric(15,2))
    mon_cuenta_id = db.Column(db.String(3))
    imp_mon_cuenta = db.Column(db.Numeric(15,2))
    imp_inv_mon_cuenta = db.Column(db.Numeric(15,2))

    
