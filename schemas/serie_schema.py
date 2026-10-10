from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Literal

class MarketStackLoad(BaseModel):
    cod_symbol: str

class InvestingLoaderResumenParams(BaseModel):
    cod_symbol: str

class SeriesSynchronizationRequest(BaseModel):
    market_data_provider: str = Field(..., min_length=1)
    cod_symbol: str = Field(..., min_length=1)
    fch_desde: date
    fch_hasta: date
    modo_carga: Literal["APPEND", "OVERWRITE", "REPLACE"]

    @field_validator("fch_desde", "fch_hasta", mode="before")
    @classmethod
    def validate_fechas(cls, v, info):
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError(f"Formato inválido para '{info.field_name}': '{v}'. Debe ser YYYY-MM-DD")
        raise ValueError(f"El parámetro '{info.field_name}' debe ser una fecha o cadena en formato YYYY-MM-DD")

    @field_validator("modo_carga", mode="before")
    @classmethod
    def validate_modo_carga(cls, v):
        if isinstance(v, str):
            v_upper = v.upper()
            if v_upper in ["APPEND", "OVERWRITE", "REPLACE"]:
                return v_upper
        raise ValueError("Valores permitidos para 'modo_carga': APPEND, OVERWRITE, REPLACE")