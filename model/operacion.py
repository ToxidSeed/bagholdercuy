from app import db

class OperacionModel(db.Model):
    __tablename__ = 'tb_operacion'

    id_operacion = db.Column(db.Integer,primary_key=True,nullable=False)
    id_cuenta = db.Column(db.Integer,nullable=False)
    fch_operacion = db.Column(db.Date,nullable=False)
    num_operacion = db.Column(db.Integer,nullable=False)
    num_variacion_posicion = db.Column(db.Integer,nullable=False)
    id_tipo_operacion = db.Column(db.Integer,nullable=False)
    id_symbol = db.Column(db.Integer,nullable=False)
    id_contrato_opcion = db.Column(db.Integer)
    cantidad = db.Column(db.Integer,nullable=False)
    imp_accion = db.Column(db.Numeric(17,3))
    imp_operacion = db.Column(db.Numeric(17,3))
    id_cuenta_destino = db.Column(db.Integer)
    ctd_posicion = db.Column(db.Integer,nullable=False)
    dsc_glosa_operacion = db.Column(db.String(150))
    fch_registro = db.Column(db.Date,nullable=False)