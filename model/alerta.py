from app import db

class AlertaModel(db.Model):
    __tablename__ = 'tb_alerta'

    id_alerta = db.Column(db.Integer,primary_key=True,nullable=False)
    id_config_alerta = db.Column(db.Integer,nullable=False)
    id_symbol = db.Column(db.Integer,nullable=False)
    imp_alerta = db.Column(db.Numeric(15,3))
    fch_registro = db.Column(db.Date)