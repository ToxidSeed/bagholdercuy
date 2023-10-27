from app import db
from datetime import date

class PosicionModel(db.Model):
    __tablename__ = 'tb_posicion'
    
    id_posicion = db.Column(db.Integer,primary_key=True,nullable=False)
    id_cuenta = db.Column(db.Integer,nullable=False)
    id_symbol = db.Column(db.Integer,nullable=False)
    id_contrato_opcion = db.Column(db.Integer)
    id_ultima_operacion = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    imp_promedio = db.Column(db.Numeric(17,2))
    imp_maximo = db.Column(db.Numeric(17,2))
    imp_minimo = db.Column(db.Numeric(17,2))
    fch_registro = db.Column(db.Date)
    fch_ultima_actualizacion = db.Column(db.Date)

