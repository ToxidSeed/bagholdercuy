import enum
from sqlalchemy import (
    Column, String, DateTime, Numeric,
    ForeignKey, Boolean
)
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from datetime import datetime

from app import db
from .types import BinaryUUID

class CategoriaActivo(enum.Enum):
    OPCIONES='Equity and Index Options'
    ACCIONES='Stocks'
    

class CodigoOperacionIBKR(enum.Enum):
    OPEN = "O"
    CLOSE = "C"    

class IbkrOperacionImportadaModel(db.Model):
    __tablename__ = "tb_ibkr_operacion_importada"

    id_operacion_importada = Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    id_importacion = db.Column(
        BinaryUUID,
        ForeignKey("tb_importacion.id_importacion"),
        nullable=False
    )

    # Datos IBKR RAW
    categoria_activo = db.Column(String(50), nullable=False)
    cod_moneda = db.Column(String(3), nullable=False)
    cod_symbol = db.Column(String(50), nullable=False)

    fch_hora_operacion = db.Column(DateTime, nullable=False)

    cantidad = db.Column(Numeric(18, 6), nullable=False)
    precio_trade = db.Column(Numeric(18, 6))
    precio_cierre = db.Column(Numeric(18, 6))

    importe_bruto = db.Column(Numeric(20, 6))
    comision = db.Column(Numeric(20, 6))
    base_costo = db.Column(Numeric(20, 6))

    pl_realizado = db.Column(Numeric(20, 6))
    pl_mtm = db.Column(Numeric(20, 6))

    codigo = db.Column(String(20))

    # Control procesamiento
    procesado = db.Column(Boolean, default=False, nullable=False)
    fch_procesado = db.Column(DateTime)

    fch_registro = db.Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relación inversa
    importacion = relationship(
        "ImportacionModel",
        back_populates="ibkr_operaciones"
    )

    id_transaccion = db.Column(
        BinaryUUID,
        ForeignKey("tb_transaccion.id_transaccion"),
        nullable=True
    )