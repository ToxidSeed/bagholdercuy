from pydantic import BaseModel, Field, model_validator
from typing import Optional


class IbkrContractMapSyncRequest(BaseModel):
    id_symbol: Optional[int] = Field(
        default=None,
        description="Identificador del símbolo en tb_symbol",
    )
    cod_symbol: Optional[str] = Field(
        default=None,
        description="Código o ticker del símbolo (ej: AAPL)",
    )
    exchange: Optional[str] = Field(
        default=None,
        description="Bolsa o exchange preferido (ej: SMART, NASDAQ)",
    )

    @model_validator(mode="after")
    def validate_identifier(self):
        has_id = self.id_symbol is not None and self.id_symbol > 0
        has_symbol = bool(self.cod_symbol and str(self.cod_symbol).strip())
        if not (has_id or has_symbol):
            raise ValueError(
                "Debe proporcionar al menos 'id_symbol' o 'cod_symbol' para sincronizar el contrato."
            )
        return self


class IbkrContractMapFilterRequest(BaseModel):
    id_symbol: Optional[int] = Field(
        default=None,
        description="Filtrar por id_symbol",
    )
    id_contrato_opcion: Optional[int] = Field(
        default=None,
        description="Filtrar por id_contrato_opcion",
    )
    conid: Optional[int] = Field(
        default=None,
        description="Filtrar por conid de IBKR",
    )
    cod_symbol: Optional[str] = Field(
        default=None,
        description="Filtrar por ticker cod_symbol",
    )
    page: Optional[int] = Field(
        default=1,
        ge=1,
        description="Número de página (>= 1)",
    )
    page_size: Optional[int] = Field(
        default=50,
        ge=1,
        le=500,
        description="Tamaño de página (1 a 500)",
    )
