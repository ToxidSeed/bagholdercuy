from config.extensions import db
from datetime import datetime


class SymbolTypeModel(db.Model):
    __tablename__ = 'tb_symbol_type'

    id_symbol_type = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_symbol_type = db.Column(db.String(15))
    nom_symbol_type = db.Column(db.String(50))
    fch_hr_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SymbolType {self.id_symbol_type} - {self.nom_symbol_type}>"
