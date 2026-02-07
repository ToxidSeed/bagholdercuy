from app import db
from datetime import datetime
import uuid
from .types import BinaryUUID

"""

"""

class MovimientoSaldoModel(db.Model):
    __tablename__ = 'tb_movimiento_saldo'

    # Clave primaria como BINARY(16)
    # Clave primaria (BINARY 16)
    id_movimiento_saldo = db.Column(BinaryUUID, primary_key=True, default=uuid.uuid4)

    # FK a la transacción que abrió (ej: compra)
    id_transaccion_apertura = db.Column(BinaryUUID, nullable=False)

    # FK a la transacción que cerró (ej: venta)
    id_transaccion_cierre = db.Column(BinaryUUID, nullable=False)

    # Cantidad aplicada de la transacción de cierre contra la apertura
    ctd_aplicada = db.Column(db.Numeric(15, 3), nullable=False)

    # Saldo restante en la transacción de apertura justo después de aplicar ctd_aplicada
    ctd_saldo_final_apertura = db.Column(db.Numeric(15, 3), nullable=False)

    # Ganancia/pérdida de ESTE match
    imp_ganancia = db.Column(db.Numeric(17, 2), nullable=False, default=0)

    # Registro de tiempo
    fch_hr_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<MovimientoSaldo {self.id_transaccion_apertura} -> {self.id_transaccion_cierre}>'