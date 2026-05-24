from app import db
from datetime import datetime
import uuid
from .types import BinaryUUID

class TransaccionSaldoModel(db.Model):
    __tablename__ = 'tb_transaccion_saldo'

    """
    Tabla que almacena los saldos de las transacciones.
    """

    # Clave primaria (BINARY 16)
    # Clave primaria (BINARY 16)
    id_transaccion = db.Column(BinaryUUID, db.ForeignKey('tb_transaccion.id_transaccion'), primary_key=True)
    
    transaccion = db.relationship("TransaccionModel", backref=db.backref("saldo", uselist=False))

    # Métricas y Valores
    # ctd_saldo: decimal(15,3)
    ctd_saldo = db.Column(db.Numeric(15, 3), nullable=False)
    
    # imp_saldo: decimal(17,2)
    imp_saldo = db.Column(db.Numeric(17, 2), nullable=False, default=0)

    # Auditoría
    fch_hr_audit = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<TransaccionSaldo {self.id_transaccion}>'