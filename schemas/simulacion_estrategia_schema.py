from datetime import date
from decimal import Decimal
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, model_validator


class SimulacionEstrategiaIdRequest(BaseModel):
    id_simulacion_estrategia: int = Field(..., gt=0)


class SimulacionPataCreateRequest(BaseModel):
    id_contrato_opcion: Optional[int] = Field(default=None, gt=0)
    cod_symbol: str = Field(..., min_length=1, max_length=50)
    tipo_opcion: Literal["CALL", "PUT"]
    fecha_vencimiento: date
    strike: Decimal = Field(..., gt=0, max_digits=18, decimal_places=6)
    posicion: Literal["LONG", "SHORT"]
    cantidad: int = Field(default=1, gt=0)
    multiplicador: int = Field(default=100, gt=0)
    precio_apertura: Optional[Decimal] = Field(
        default=None, ge=0, max_digits=18, decimal_places=6
    )
    moneda_id: str = Field(default="USD", min_length=3, max_length=3)


class SimulacionGrupoCreateRequest(BaseModel):
    orden: int = Field(..., ge=1, le=32767)
    nombre: str = Field(..., min_length=1, max_length=120)
    tipo: str = Field(default="CUSTOM", min_length=1, max_length=40)
    contratos: List[SimulacionPataCreateRequest] = Field(default_factory=list)


class SimulacionEstrategiaCreateRequest(BaseModel):
    id_subyacente_symbol: Optional[int] = Field(default=None, gt=0)
    cod_subyacente: Optional[str] = Field(default=None, min_length=1, max_length=20)
    nombre: str = Field(..., min_length=1, max_length=120)
    etiqueta: str = Field(default="ESTRATEGIA", min_length=1, max_length=40)
    notas: Optional[str] = None
    moneda_id: str = Field(default="USD", min_length=3, max_length=3)
    grupos: List[SimulacionGrupoCreateRequest] = Field(..., min_length=1)

    @model_validator(mode="after")
    def validar_estrategia(self):
        if self.id_subyacente_symbol is None and not self.cod_subyacente:
            raise ValueError("Debe proporcionar id_subyacente_symbol o cod_subyacente")
        if not any(grupo.contratos for grupo in self.grupos):
            raise ValueError("La estrategia debe contener al menos una pata de opción")
        ordenes = [grupo.orden for grupo in self.grupos]
        if len(ordenes) != len(set(ordenes)):
            raise ValueError("El orden de los grupos no puede repetirse")
        return self
