from app import db
from datetime import datetime

class InstrumentoFinancieroModel(db.Model):
    __tablename__ = 'tb_instrumento_financiero'

    id_instrumento_financiero = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_instrumento_financiero = db.Column(db.String(15))
    nom_instrumento_financiero = db.Column(db.String(50))
    fch_hr_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<InstrumentoFinanciero {self.id_instrumento_financiero} - {self.nom_instrumento_financiero}>"
