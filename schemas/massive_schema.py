from pydantic import BaseModel
from typing import Optional

class MassiveSeriesLoadParams(BaseModel):
    cod_symbol: str
    fch_desde: Optional[str] = ""
    fch_hasta: Optional[str] = ""
    modo_carga: Optional[str] = "Append"
