from app import db

class TransaccionModel(db.Model):
    __tablename__ = 'tb_transaccion'

    id_transaccion = db.Column(db.Integer,primary_key=True,nullable=False)
    id_orden = db.Column(db.Integer,nullable=False)
    num_orden = db.Column(db.Integer)
    num_orden_transaccion = db.Column(db.Integer)
    id_symbol = db.Column(db.Integer)
    id_contrato_opcion = db.Column(db.Integer)
    id_subyacente = db.Column(db.Integer)
    cod_tipo_activo = db.Column(db.Integer,nullable=False)
    cod_tipo_orden = db.Column(db.String(1),nullable=False)
    cantidad = db.Column(db.Numeric(15,3),nullable=False)
    ctd_saldo_posicion = db.Column(db.Integer,nullable=False)
    fch_transaccion = db.Column(db.Date,nullable=False)
    num_mes_posicion = db.Column(db.Integer,nullable=False)
    imp_accion = db.Column(db.Numeric(17,2),nullable=False)
    imp_posicion = db.Column(db.Numeric(17,2),nullable=False)
    posicion_ref_id = db.Column(db.Integer)
    imp_accion_origen = db.Column(db.Numeric(17,2))
    imp_gp_realizada = db.Column(db.Numeric(17,2))
    fch_registro = db.Column(db.Date)
    hora_registro = db.Column(db.Time)
    usuario_id = db.Column(db.Integer)