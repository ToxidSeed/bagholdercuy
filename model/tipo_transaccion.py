from app import db
from datetime import datetime

"""
* Los tipos de transaccion actualmente son:
cod_tipo_transaccion	nom_tipo_transaccion
C	Compra
V	Venta
LE	Liquidacion en Efectivo
LF	Liquidacion Fisica
ESV	Expiracion sin valor
"""

class TipoTransaccionModel(db.Model):
    __tablename__ = 'tb_tipo_transaccion'

    id_tipo_transaccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_tipo_transaccion = db.Column(db.String(5))
    nom_tipo_transaccion = db.Column(db.String(50))
    fch_hr_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TipoTransaccion {self.cod_tipo_transaccion} - {self.nom_tipo_transaccion}>"

    