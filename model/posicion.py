from app import db

class PosicionModel(db.Model):
    __tablename__="tb_posicion"

    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer)
    num_orden = db.Column(db.Integer)
    num_posicion = db.Column(db.Integer)
    cod_symbol	= db.Column(db.String(20))
    cod_opcion = db.Column(db.String(30))
    cod_tipo_activo = db.Column(db.Integer)
    cod_tipo_orden = db.Column(db.String(1))
    cantidad = db.Column(db.Numeric(15,3))
    fch_transaccion = db.Column(db.Date)
    num_mes_posicion = db.Column(db.Integer)
    imp_accion = db.Column(db.Numeric(17,2))
    imp_posicion = db.Column(db.Numeric(17,2))    
    posicion_ref_id = db.Column(db.Integer)    
    ctd_saldo_posicion = db.Column(db.Integer)
    imp_accion_origen = db.Column(db.Numeric(17,2))
    imp_gp_realizada = db.Column(db.Numeric(17,2))    
    fch_registro = db.Column(db.Date)
    hora_registro = db.Column(db.Time)
    usuario_id = db.Column(db.Integer)
    
    
