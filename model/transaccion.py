from app import db

class TransaccionModel(db.Model):
    __tablename__ = 'tb_transaccion'

    id_transaccion = db.Column(db.Integer,primary_key=True,nullable=False)
    id_orden = db.Column(db.Integer,nullable=False)
    num_orden = db.Column(db.Integer)
    num_orden_transaccion = db.Column(db.Integer)
    id_symbol = db.Column(db.Integer)
    id_contrato_opcion = db.Column(db.Integer)    
    cod_tipo_activo = db.Column(db.Integer,nullable=False)    
    cantidad = db.Column(db.Numeric(15,3),nullable=False)
    ctd_saldo_transaccion = db.Column(db.Integer,nullable=False)
    fch_transaccion = db.Column(db.Date,nullable=False)
    cod_mes_transaccion = db.Column(db.Integer,nullable=False)     
    cod_semana_transaccion = db.Column(db.Integer,nullable=False)
    imp_accion = db.Column(db.Numeric(17,2),nullable=False)
    imp_transaccion = db.Column(db.Numeric(17,2),nullable=False)
    id_transaccion_ref = db.Column(db.Integer)
    imp_accion_origen = db.Column(db.Numeric(17,2))
    imp_rentabilidad = db.Column(db.Numeric(17,2))
    fch_registro = db.Column(db.Date)
    hora_registro = db.Column(db.Time)
    id_cuenta = db.Column(db.Integer)