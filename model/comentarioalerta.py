from app import db


class ComentarioAlertaModel(db.Model):
    __tablename__ = 'tb_comentario_alerta'

    id_comentario_alerta = db.Column(db.Integer,primary_key=True,nullable=False)
    id_alerta = db.Column(db.Integer)
    dsc_comentario = db.Column(db.String(250))
    fch_registro = db.Column(db.Date)
    fch_actualizacion = db.Column(db.DateTime)
