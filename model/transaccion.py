from config.extensions import db
from datetime import datetime
from .types import BinaryUUID
import uuid

"""
Las transacciones son registros que se hacen cada vez que se hace una operación sobre un activo, estos tipos de operaciones estan definidos en la tabla tb_tipo_transaccion.
num_transaccion: es un correlativo secuencial del 1 al N, que se reinicia cada dia.
"""


class TransaccionModel(db.Model):
    __tablename__ = 'tb_transaccion'

    id_transaccion = db.Column(BinaryUUID, primary_key=True, default=uuid.uuid4)
    id_transaccion_origen = db.Column(BinaryUUID, nullable=True)
    
    id_cuenta = db.Column(db.Integer, nullable=False)    
    cod_symbol = db.Column(db.String(25), nullable=False)
    
    id_instrumento_financiero = db.Column(
        db.Integer,
        db.ForeignKey('tb_instrumento_financiero.id_instrumento_financiero'),
        nullable=True
    )
    id_tipo_transaccion = db.Column(
        db.Integer,
        db.ForeignKey('tb_tipo_transaccion.id_tipo_transaccion'),
        nullable=False
    )
    
    id_indicador_apcierre = db.Column(
        db.Integer,
        db.ForeignKey('tb_indicador_apcierre.id_indicador_apcierre'),
        nullable=False
    )
    id_evento_origen = db.Column(db.Integer, db.ForeignKey('tb_evento_origen.id_evento_origen'), nullable=False)

    instrumento_financiero = db.relationship('InstrumentoFinancieroModel')
    tipo_transaccion = db.relationship('TipoTransaccionModel')
    indicador_apcierre = db.relationship('IndicadorApcierreModel')
    evento_origen = db.relationship('EventoOrigenModel')
    
    fch_hr_transaccion = db.Column(db.DateTime, nullable=False)
    orden_fifo = db.Column(db.Integer, nullable=False)
    ind_requiere_revision = db.Column(db.SmallInteger, nullable=False)
    
    cantidad = db.Column(db.Numeric(15, 3), nullable=False)
    imp_unitario = db.Column(db.Numeric(17, 2), nullable=False)
    imp_bruto = db.Column(db.Numeric(17, 2), nullable=False)
    
    fch_hr_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Transaccion {self.id_transaccion} - {self.cod_symbol} - {self.fch_hr_transaccion}>"


