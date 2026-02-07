from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal

class OrdenManagerEjecutarParams(BaseModel):
    cod_symbol: str    
    id_instrumento_financiero: int
    id_tipo_transaccion: int
    cantidad: Decimal = Field(max_digits=15, decimal_places=2)
    imp_accion: Decimal = Field(max_digits=15, decimal_places=2)
    fch_transaccion: date    
    