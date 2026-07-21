from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class VariacionDiariaSearchRequest(BaseModel):
    symbol: str = Field(min_length=1)
    fch_desde: Optional[date] = None
    fch_hasta: Optional[date] = None
