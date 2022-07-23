from app import db

class TransaccionFondosModel(db.Model):
    __tablename__="tb_transaccion_fondos"

    id = db.Column(db.Integer,primary_key=True)
    fec_transaccion = db.Column(db.Date)
    num_transaccion = db.Column(db.Integer)    
    tipo_trans_id = db.Column(db.Integer)    
    imp_transaccion = db.Column(db.Numeric(15,2))
    mon_trans_id = db.Column(db.String(3))
    mon_dest_conv_id = db.Column(db.String(3))
    imp_tc_conv = db.Column(db.Numeric(15,3))
    imp_dest_conv = db.Column(db.Numeric(15,2))
    user_id = db.Column(db.Integer)
    fec_registro = db.Column(db.Date)
    fec_audit = db.Column(db.DateTime)
    