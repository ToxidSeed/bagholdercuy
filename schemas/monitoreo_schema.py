from pydantic import BaseModel, Field, model_validator
from typing import Optional, Any
from model.monitoreo import MonitoreoModel


class MonitoreoGetRequest(BaseModel):
    id_cuenta: int = Field(..., description="ID de la cuenta a consultar")
    id_symbol: Optional[int] = Field(default=None, description="Filtrar por symbol")
    id_contrato_opcion: Optional[int] = Field(
        default=None, description="Filtrar por contrato de opción"
    )
    id_symbol_type: Optional[int] = Field(
        default=None, description="Filtrar por tipo de symbol"
    )

    def to_opcionales(self) -> dict:
        opcionales = {}
        if self.id_symbol is not None:
            opcionales["id_symbol"] = self.id_symbol
        if self.id_contrato_opcion is not None:
            opcionales["id_contrato_opcion"] = self.id_contrato_opcion
        if self.id_symbol_type is not None:
            opcionales["id_symbol_type"] = self.id_symbol_type
        return opcionales


class MonitoreoRegistrarRequest(BaseModel):
    id_cuenta: int = Field(..., description="ID de la cuenta donde se registra el monitoreo")
    id_symbol: Optional[int] = Field(default=None, description="ID del símbolo a monitorear")
    id_symbol_subyacente: Optional[int] = Field(
        default=None, description="ID del símbolo subyacente para contrato de opción"
    )
    id_contrato_opcion: Optional[int] = Field(
        default=None, description="ID del contrato de opción a monitorear"
    )
    id_symbol_type: Optional[int] = Field(default=None, description="Tipo de símbolo")

    # Campos opcionales para registrar/resolver contrato de opción al vuelo
    cod_symbol: Optional[str] = Field(default=None, description="Ticker o código OSI")
    tipo_opcion: Optional[str] = Field(default=None, description="CALL o PUT")
    fch_vencimiento: Optional[Any] = Field(default=None, description="Fecha de vencimiento")
    imp_strike: Optional[float] = Field(default=None, description="Precio strike")
    tam_contrato: Optional[int] = Field(default=100, description="Tamaño del contrato")
    cod_moneda: Optional[str] = Field(default="USD", description="Moneda del contrato")
    descripcion: Optional[str] = Field(default=None, description="Descripción del contrato")
    conid: Optional[int] = Field(default=None, description="Conid de IBKR si está disponible")

    @model_validator(mode="after")
    def validate_symbol_o_contrato(self):
        es_opcion = (
            self.id_contrato_opcion is not None
            or self.id_symbol_type == 2
            or (self.tipo_opcion and str(self.tipo_opcion).upper() in ("CALL", "PUT"))
            or (self.cod_symbol and (self.tipo_opcion or self.fch_vencimiento or self.imp_strike))
        )
        if self.id_symbol is None and self.id_symbol_subyacente is None and not es_opcion:
            raise ValueError("Debe enviar 'id_symbol' o 'id_contrato_opcion'")
        return self

    def to_model(self) -> MonitoreoModel:
        monitoreo = MonitoreoModel()
        monitoreo.id_cuenta = self.id_cuenta

        if self.id_contrato_opcion is None and (
            self.id_symbol_type == 2
            or (self.tipo_opcion and str(self.tipo_opcion).upper() in ("CALL", "PUT"))
            or (self.cod_symbol and (self.tipo_opcion or self.fch_vencimiento or self.imp_strike))
        ):
            subyacente_id = self.id_symbol_subyacente or self.id_symbol
            monitoreo.contrato_opcion_data = {
                "id_symbol_subyacente": subyacente_id,
                "id_symbol": subyacente_id,
                "cod_symbol": self.cod_symbol,
                "tipo_opcion": self.tipo_opcion,
                "fch_vencimiento": self.fch_vencimiento,
                "imp_strike": self.imp_strike,
                "tam_contrato": self.tam_contrato or 100,
                "cod_moneda": self.cod_moneda or "USD",
                "descripcion": self.descripcion,
                "conid": self.conid,
            }
            monitoreo.id_symbol_type = 2
            monitoreo.id_symbol = None
        else:
            monitoreo.id_symbol = self.id_symbol
            monitoreo.id_contrato_opcion = self.id_contrato_opcion
            monitoreo.id_symbol_type = self.id_symbol_type

        monitoreo.conid = self.conid
        return monitoreo
