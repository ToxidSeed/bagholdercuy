from app import db

class ConversionModel(db.Model):
    __tablename__="tb_conversion_moneda"

    id = db.Column(db.Integer, primary_key=True)
    fec_transaccion = db.Column(db.Date)
    moneda_base_symbol = db.Column(db.String(3))
    moneda_ref_symbol = db.Column(db.String(3))
    importe_conversion = db.Column(db.Numeric(15,2))
    tipo_operacion = db.Column(db.String(1))
    importe_tc = db.Column(db.Numeric(15,2))
    importe_post_conversion = db.Column(db.Numeric(15,))
    fec_registro = db.Column(db.Date)
    fec_audit = db.Column(db.DateTime)
