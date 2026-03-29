from pydantic import BaseModel, Field, model_validator
from datetime import date
from decimal import Decimal
from constants.instrumento_financiero import get_instrumento_financiero

class OrdenManagerEjecutarParams(BaseModel):
    cod_symbol: str    
    id_instrumento_financiero: int
    id_tipo_transaccion: int
    cantidad: Decimal = Field(max_digits=15, decimal_places=2)
    imp_accion: Decimal = Field(max_digits=15, decimal_places=2)
    fch_transaccion: date    
    id_contrato_opcion: int = Field(default=None)


    @model_validator(mode='after')
    def validate_contrato_opcion(self):
        if self.id_instrumento_financiero == get_instrumento_financiero().OPTION and self.id_contrato_opcion is None:
            raise ValueError("id_contrato_opcion es obligatorio cuando id_instrumento_financiero es 2")
        return self
    