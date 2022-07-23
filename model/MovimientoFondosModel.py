from app import db

class MovimientoFondosModel(db.Model):
    __tablename__="tb_mov_fondos"

    id = db.Column(db.Integer,primary_key=True)
    trans_id = db.Column(db.Integer)
    ref_mov_id = db.Column(db.Integer)
    tipo_trans_id = db.Column(db.String(1))
    tipo_mov_id = db.Column(db.String(1))
    imp_mov = db.Column(db.Numeric(15,2))
    mon_mov_id = db.Column(db.String(3))
    imp_saldo_mov = db.Column(db.Numeric(15,2))
    mon_cuenta_id = db.Column(db.String(3))
    imp_tc_cuenta = db.Column(db.Numeric(15,3))
    imp_saldo_cuenta = db.Column(db.Numeric(15,2))
    imp_tc_usd = db.Column(db.Numeric(15,3))
    imp_saldo_cuenta_usd = db.Column(db.Numeric(15,2))
    fch_audit = db.Column(db.DateTime)
