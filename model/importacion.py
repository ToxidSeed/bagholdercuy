import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Integer, DateTime,
    Enum, ForeignKey, CHAR
)
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship
from config.extensions import db
from .types import BinaryUUID


# ==========================
# ENUMS
# ==========================

class OrigenImportacion(enum.Enum):
    IBKR = "IBKR"
    SURA = "SURA"
    HAPI = "HAPI"


class TipoDataset(enum.Enum):
    TRADES = "TRADES"
    CASH = "CASH"
    HOLDINGS = "HOLDINGS"
    DIVIDENDS = "DIVIDENDS"


class EstadoImportacion(enum.Enum):
    PENDIENTE = "PENDIENTE"
    PROCESANDO = "PROCESANDO"
    PROCESADO = "PROCESADO"
    ERROR = "ERROR"


# ==========================
# MODELO
# ==========================

class ImportacionModel(db.Model):
    __tablename__ = "tb_importacion"

    id_importacion = db.Column(BinaryUUID, primary_key=True, default=uuid.uuid4)

    cod_origen = db.Column(
        Enum(OrigenImportacion),
        nullable=False
    )


    tipo_dataset = db.Column(
        Enum(TipoDataset),
        nullable=False
    )

    nombre_archivo = db.Column(String(255))
    hash_archivo = db.Column(CHAR(64))

    total_registros = db.Column(Integer, default=0)
    registros_ok = db.Column(Integer, default=0)
    registros_error = db.Column(Integer, default=0)

    estado = db.Column(
        Enum(EstadoImportacion),
        default=EstadoImportacion.PENDIENTE,
        nullable=False
    )

    fch_importacion = db.Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    fch_procesado = db.Column(DateTime)

    # Relación con IBKR
    ibkr_operaciones = relationship(
        "IbkrOperacionImportadaModel",
        back_populates="importacion",
        cascade="all, delete-orphan"
    )