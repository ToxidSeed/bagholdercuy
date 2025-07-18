from pydantic import BaseModel
from datetime import date

class CicloGetCiclosDiarios(BaseModel):
    cod_symbol: str
    fch_desde: date
    fch_hasta: date

class CicloVariacionGetCiclosDiarios(BaseModel):
    cod_symbol: str
    fch_desde: date
    fch_hasta: date