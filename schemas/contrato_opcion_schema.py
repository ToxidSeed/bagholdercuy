from datetime import date
from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator


class ContratoOpcionFiltroRequest(BaseModel):
    id_contrato_opcion: Optional[int] = Field(
        default=None, description="ID del contrato de opción"
    )
    cod_symbol: Optional[str] = Field(
        default=None, description="Código de ticker subyacente o contrato"
    )
    id_symbol_subyacente: Optional[int] = Field(
        default=None, description="ID del símbolo subyacente"
    )
    sentidos: Optional[Union[List[str], str]] = Field(
        default_factory=list, description="Sentido(s) de opción: CALL, PUT"
    )
    fch_expiracion: Optional[Union[date, str]] = Field(
        default=None, description="Fecha de expiración (YYYY-MM-DD)"
    )
    imp_ejercicio: Optional[float] = Field(
        default=None, description="Precio strike"
    )
    limit: Optional[int] = Field(default=200, ge=0, description="Límite de registros")

    @field_validator("id_contrato_opcion", mode="before")
    @classmethod
    def parse_id(cls, v):
        if v in (None, ""):
            return None
        return int(v)

    @field_validator("fch_expiracion", mode="before")
    @classmethod
    def parse_fecha(cls, v):
        if v in (None, ""):
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            v_str = v.strip()
            return date.fromisoformat(v_str) if v_str else None
        return v

    @field_validator("imp_ejercicio", mode="before")
    @classmethod
    def parse_float(cls, v):
        if v in (None, ""):
            return None
        return float(v)

    @field_validator("sentidos", mode="before")
    @classmethod
    def parse_sentidos(cls, v):
        if v in (None, ""):
            return []
        if isinstance(v, str):
            parts = [s.strip().upper() for s in v.split(",") if s.strip()]
        elif isinstance(v, (list, tuple)):
            parts = [str(s).strip().upper() for s in v if str(s).strip()]
        else:
            parts = []
        for p in parts:
            if p not in ("CALL", "PUT"):
                raise ValueError("No se ha indicado un tipo de opcion valido")
        return parts


class ContratoOpcionChainRequest(BaseModel):
    cod_symbol: str = Field(
        ..., min_length=1, description="Ticker del subyacente requerido"
    )
    fch_expiracion: Optional[Union[date, str]] = Field(
        default=None, description="Fecha de expiración"
    )
    imp_ejercicio: Optional[float] = Field(
        default=None, description="Precio strike"
    )

    @field_validator("fch_expiracion", mode="before")
    @classmethod
    def parse_fecha(cls, v):
        if v in (None, ""):
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            v_str = v.strip()
            return date.fromisoformat(v_str) if v_str else None
        return v

    @field_validator("imp_ejercicio", mode="before")
    @classmethod
    def parse_float(cls, v):
        if v in (None, ""):
            return None
        return float(v)


class ContratoOpcionCreateRequest(BaseModel):
    cod_symbol: str = Field(..., min_length=1, description="Ticker OSI del contrato")
    sentido: str = Field(..., description="CALL o PUT")
    cod_subyacente: str = Field(
        ..., min_length=1, description="Ticker o código subyacente"
    )
    fch_expiracion: Union[date, str] = Field(..., description="Fecha de expiración")
    imp_ejercicio: float = Field(..., gt=0, description="Precio strike")
    ctd_tamano_contrato: Optional[int] = Field(
        default=100, gt=0, description="Tamaño del contrato"
    )
    cod_moneda: Optional[str] = Field(default="USD", description="Moneda")
    descripcion: Optional[str] = Field(default=None, description="Descripción")

    @model_validator(mode="before")
    @classmethod
    def normalize_and_validate(cls, data):
        if not isinstance(data, dict):
            return data
        d = dict(data)

        # Aliases
        if "tipo_opcion" in d and "sentido" not in d:
            d["sentido"] = d["tipo_opcion"]
        if "cod_symbol_subyacente" in d and "cod_subyacente" not in d:
            d["cod_subyacente"] = d["cod_symbol_subyacente"]
        if "fch_vencimiento" in d and "fch_expiracion" not in d:
            d["fch_expiracion"] = d["fch_vencimiento"]
        if "imp_strike" in d and "imp_ejercicio" not in d:
            d["imp_ejercicio"] = d["imp_strike"]
        if "tam_contrato" in d and "ctd_tamano_contrato" not in d:
            d["ctd_tamano_contrato"] = d["tam_contrato"]

        # Validaciones de presencia
        if not d.get("cod_symbol"):
            raise ValueError("No se ha enviado el symbol")
        if not d.get("cod_subyacente"):
            raise ValueError("No se ha enviado el 'cod_subyacente'")
        if not d.get("fch_expiracion"):
            raise ValueError("No se ha enviado 'fch_expiracion'")
        if d.get("imp_ejercicio") in (None, "", 0):
            raise ValueError("No se ha enviado 'imp_ejercicio'")
        if d.get("ctd_tamano_contrato") in (None, "", 0):
            raise ValueError("No se ha indicado el tamaño del contrato")
        if not d.get("cod_moneda"):
            raise ValueError("No se ha indicado la moneda")

        sentido = str(d.get("sentido", "")).strip().upper()
        if sentido not in ("CALL", "PUT"):
            raise ValueError(f"el sentido {d.get('sentido')} no es valido")
        d["sentido"] = sentido

        if isinstance(d.get("fch_expiracion"), str):
            d["fch_expiracion"] = date.fromisoformat(d["fch_expiracion"].strip())

        return d


class ContratoOpcionMarketDataLoaderRequest(BaseModel):
    cod_symbol: str = Field(..., min_length=1, description="Código del subyacente")
    fch_expiracion: Union[date, str] = Field(..., description="Fecha de expiración")

    @field_validator("fch_expiracion", mode="before")
    @classmethod
    def parse_fecha(cls, v):
        if isinstance(v, str):
            return date.fromisoformat(v.strip())
        return v


class ContratoOpcionCsvLoaderRequest(BaseModel):
    cod_moneda: str = Field(default="USD", min_length=1)
    ctd_multiplicador: int = Field(default=100, gt=0)
    formato_cod_opcion: str = Field(default="OSI", min_length=1)
    flg_excluir_errores: bool = Field(default=True)
