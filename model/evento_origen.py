from app import db
from datetime import datetime

class EventoOrigenModel(db.Model):
    __tablename__ = 'tb_evento_origen'

    id_evento_origen = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_evento = db.Column(db.String(5), nullable=False, unique=True)
    nom_evento = db.Column(db.String(50), nullable=False)
    fch_hr_registro = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<EventoOrigen {self.cod_evento}>'
