from app import db

class ConversionMonedaModel(db.Model):
    __tablename__="tb_conversion_moneda"

    id = db.Column(db.Integer, primary_key=True)
    transaccion_id = db.Column(db.Integer)
    fch_conversion = db.Column(db.Date)
    mon_ori_id = db.Column(db.String(3))
    mon_dest_id = db.Column(db.String(3))
    imp_tc = db.Column(db.Numeric(15,3))
    operacion_id = db.Column(db.String(3))
    imp_origen = db.Column(db.Numeric(15,2))
    imp_convertido = db.Column(db.Numeric(15,2))
    fch_registro = db.Column(db.Date)
    usuario_id = db.Column(db.Integer)
    fch_audit = db.Column(db.DateTime)
    