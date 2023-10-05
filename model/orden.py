from app import db

class OrdenModel(db.Model):
    __tablename__ = "tb_orden"

    orden_id = db.Column(db.Integer, primary_key=True)
    num_orden = db.Column(db.Integer)
    cod_tipo_orden = db.Column(db.String(1))
    cod_symbol = db.Column(db.String(20))
    cod_opcion = db.Column(db.String(30))
    cod_tipo_activo = db.Column(db.String(20))
    cantidad = db.Column(db.Integer)
    imp_accion = db.Column(db.Numeric(15,4))
    usuario_id = db.Column(db.Integer)
    fch_registro = db.Column(db.Date)
    fch_orden = db.Column(db.Date)    
