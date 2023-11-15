from app import db

class AlertaModel(db.Model):
    __tablename__ = 'tb_alerta'

    id_alerta = db.Column(db.Integer,primary_key=True,nullable=False)
    id_config_alerta = db.Column(db.Integer,nullable=False)
    id_symbol = db.Column(db.Integer,nullable=False)
    imp_alerta = db.Column(db.Numeric(15,3))
    imp_ejercicio_compra_call = db.Column(db.Numeric(15,3))
    imp_ejercicio_venta_call = db.Column(db.Numeric(15,3))
    imp_ejercicio_compra_put = db.Column(db.Numeric(15,3))
    imp_ejercicio_venta_put = db.Column(db.Numeric(15,3))
    num_dias_expiracion_call = db.Column(db.Integer)
    num_dias_expiracion_put = db.Column(db.Integer)