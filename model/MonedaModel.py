from app import db

class MonedaModel(db.Model):
    __tablename__="tb_moneda"

    moneda_id = db.Column(db.String(3), primary_key=True)
    codigo_iso = db.Column(db.String(3))
    simbolo = db.Column(db.String(5))
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(250))
    fec_registro = db.Column(db.Date)
    fec_audit = db.Column(db.DateTime)