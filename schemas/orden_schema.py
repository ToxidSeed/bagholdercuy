from pydantic import BaseModel, Field, model_validator
from datetime import date
from decimal import Decimal
from constants.symbol_type import get_symbol_type


class OrdenManagerEjecutarParams(BaseModel):
    cod_symbol: str    
    id_symbol_type: int
    id_tipo_transaccion: int
    cantidad: Decimal = Field(max_digits=15, decimal_places=2)
    imp_accion: Decimal = Field(max_digits=15, decimal_places=2)
    fch_hr_transaccion: date    
    id_contrato_opcion: int = Field(default=None)


    @model_validator(mode='after')
    def validate_contrato_opcion(self):
        if self.id_symbol_type == get_symbol_type().OPTION and self.id_contrato_opcion is None:
            raise ValueError("id_contrato_opcion es obligatorio cuando id_symbol_type es 2")
        return self
    