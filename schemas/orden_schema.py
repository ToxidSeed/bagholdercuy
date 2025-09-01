from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class OrdenManagerEjecutarParams(BaseModel):
    cod_symbol: str
    cod_symbol_opcion: Optional[str] = None
    cod_tipo_orden: str
    cantidad: Decimal = Field(max_digits=15, decimal_places=2)
    imp_accion: Decimal = Field(max_digits=15, decimal_places=2)
    fch_orden: date
    fch_registro: date 