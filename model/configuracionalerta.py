from app import db


class ConfiguracionAlertaModel(db.Model):
    __tablename__ = 'tb_configuracion_alerta'

    id_config_alerta = db.Column(db.Integer,primary_key=True,nullable=False)
    id_monitoreo = db.Column(db.Integer,nullable=False)
    id_cuenta = db.Column(db.Integer,nullable=False)
    id_symbol = db.Column(db.Integer)
    ctd_variacion_imp_accion = db.Column(db.Integer)
    cod_tipo_variacion_imp_accion = db.Column(db.Integer)
    ctd_ciclos = db.Column(db.Integer)
    imp_inicial_ciclos = db.Column(db.Numeric(15,3))