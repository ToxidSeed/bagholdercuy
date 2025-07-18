from pydantic import BaseModel
from datetime import date

class MarketStackLoad(BaseModel):
    cod_symbol: str