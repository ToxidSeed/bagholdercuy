from app import db

class ConfiguracionAlertaModel(db.Model):
    __tablename__ = 'tb_configuracion_alerta'

    id_config_alerta = db.Column(db.Integer,primary_key=True,nullable=False)
    id_monitoreo = db.Column(db.Integer)
    id_cuenta = db.Column(db.Integer)
    id_symbol = db.Column(db.Integer)
    flg_compras = db.Column(db.Integer)
    flg_ventas = db.Column(db.Integer)
    ctd_variacion_titulo = db.Column(db.Integer)
    cod_tipo_variacion_titulo = db.Column(db.Integer)
    ctd_ciclos = db.Column(db.Integer)
    imp_inicio_ciclos = db.Column(db.Numeric(15,3))
    flg_opciones = db.Column(db.Integer)
    cod_tipo_variacion_ejercicio = db.Column(db.Integer)
    imp_fijo_ejercicio_call = db.Column(db.Numeric(15,3))
    imp_fijo_ejercicio_put = db.Column(db.Numeric(15,3))
    imp_variacion_subyacente_call = db.Column(db.Numeric(15,3))
    imp_variacion_subyacente_put = db.Column(db.Numeric(15,3))
    num_dias_expiracion_call = db.Column(db.Integer)
    num_dias_expiracion_put = db.Column(db.Integer)