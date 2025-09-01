from pydantic import BaseModel
from datetime import date

class MarketStackLoad(BaseModel):
    cod_symbol: str

class InvestingLoaderResumenParams(BaseModel):
    cod_symbol: str