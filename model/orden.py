from app import db
from model.posicion import PosicionModel
from datetime import date

class OrdenModel(db.Model):
    __tablename__ = 'tb_orden'
    
    id_orden = db.Column(db.Integer,primary_key=True,nullable=False)
    id_operacion = db.Column(db.Integer)
    id_cuenta = db.Column(db.Integer,nullable=False)
    num_orden = db.Column(db.Integer)
    cod_tipo_orden = db.Column(db.String(1))
    id_symbol = db.Column(db.Integer)
    id_contrato_opcion = db.Column(db.Integer)    
    cod_tipo_activo = db.Column(db.String(20))
    cantidad = db.Column(db.Integer)
    imp_accion = db.Column(db.Numeric(17,2))
    fch_registro = db.Column(db.Date)
    fch_orden = db.Column(db.Date)

    def a_posicion(self):
        posicion = PosicionModel(
            id_cuenta = self.id_cuenta,
            id_symbol = self.id_symbol,
            id_contrato_opcion = self.id_contrato_opcion,
            cantidad = 0,
            imp_promedio = 0,
            imp_maximo = 0,
            imp_minimo = 0,
            fch_registro = date.today(),
            fch_actualizacion = date.today()
        )
        
        return posicion