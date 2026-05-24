from app import db
from datetime import datetime

class IndicadorApcierreModel(db.Model):
    __tablename__ = 'tb_indicador_apcierre'

    id_indicador_apcierre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_indicador = db.Column(db.String(5), nullable=False, unique=True)
    nom_indicador = db.Column(db.String(50), nullable=False)
    fch_hr_registro = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<IndicadorApcierre {self.cod_indicador}>'
