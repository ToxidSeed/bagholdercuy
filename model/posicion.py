from app import db
from datetime import date

class PosicionModel(db.Model):
    __tablename__ = 'tb_posicion'
    
    id_transaccion = db.Column(db.Integer,primary_key=True,nullable=False)
    id_cuenta = db.Column(db.Integer,nullable=False)
    cod_symbol = db.Column(db.String,nullable=False)
    cod_symbol_opcion = db.Column(db.String)
    fch_transaccion = db.Column(db.Date)
    num_transaccion = db.Column(db.Integer)
    cantidad = db.Column(db.Numeric(17,2))
    imp_accion = db.Column(db.Numeric(17,2))
    imp_posicion = db.Column(db.Numeric(17,2))
    fch_registro = db.Column(db.Date)
    fch_ult_actualizacion = db.Column(db.Date)

